#!/usr/bin/env python3

# ReapAir is a tool to generate and distribute useful repair instructions for your everyday life.
# Copyright (C) 2020  ReapAir developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import click
import datetime
import random
import sys
import math
from serial import Serial
from collections import deque
from pathlib import Path

from escpos.printer import File, Usb

from .helpers import get_sentences, get_template
from .settings import DEFAULT_TEMPLATE, ASSETS_PATH, SENTENCES

cwd = Path.cwd()


def generate_html(instructions, template_path):
    """
    Renders instructions into HTML and
    returns it as a string for further processing.
    """
    try:
        template = get_template(Path(template_path))
    except Exception as e:
        sys.exit(e)

    # TODO: randomize the person drawings
    return template.render(instructions=instructions)


def save_file(content, filepath, overwrite=False):
    """
    Take a string and save it into a file.
    The overwrite flag avoids overwriting if the file already exists.
    """
    out_path = Path(filepath)
    if out_path.exists() and not overwrite:
        raise FileExistsError(f"File {filepath} already exists and will not be overwritten.")

    with open(out_path, "w") as outfile:
        outfile.write(content)
        print(f"Saved HTML file to: {out_path}")


def generate_instructions(sentences_dict: dict, n):
    """
    Selects a mix of sentences according to a predefined distribution
    from the different lists contained in the dict.
    """
    if n < 1:
        raise ValueError(f"Value for '-n' has to be greater than 0. Received: {n}")

    if not isinstance(sentences_dict, dict):
        raise TypeError(f"'sentence_dict' must be of type 'dict', instead got '{type(sentences_dict)}'")

    safety_notes = sentences_dict["safety_notes"]
    instructions = sentences_dict["instructions"]
    conditionals = sentences_dict["conditionals"]
    finals = sentences_dict["finals"]

    if n <= 3:
        n = min(n, len(instructions))
        return random.sample(instructions, n)

    # sentence type distribution
    safety_notes_count = min(math.ceil(n * 0.2), len(safety_notes))
    conditionals_count = min(math.ceil(n * 0.1), len(conditionals))
    finals_count = 1
    instructions_count = n - (safety_notes_count + conditionals_count + finals_count)
    instructions_count = min(instructions_count, len(instructions))

    result = random.sample(safety_notes, safety_notes_count)
    inst = random.sample(instructions, instructions_count)

    # generate non-repeating indices in the range [1, len(inst)]
    random_indices = []
    while len(random_indices) < conditionals_count:
        index = random.randrange(1, len(inst), 2)
        if index not in random_indices:
            random_indices.append(index)

    cond = random.sample(conditionals, conditionals_count)

    # insert the conditional sentences into the instructions
    i = 0
    for index in random_indices:
        inst.insert(index, cond[i])
        i += 1

    result += inst
    result += random.sample(finals, finals_count)

    return result


def print_instructions(instructions):
    """
    Print instructions to a thermal printer.
    :param instructions: list of strings containing the instructions
    """

    try:
        # Vendor ID and Product ID of the 36-pin IEEE 1284 to USB converter,
        # this printer is so old it doesn't have USB directly
        printer = Usb(0x1a86, 0x7584, profile="TM-T88II")
    except Exception as e:
        print("Exception while trying to access printer via USB:")
        print(str(e))
        try:
            printer = File("/dev/usb/lp0", profile="TM-T88II")
        except FileNotFoundError as e:
            print("Received exception while trying to access printer via File:")
            print(str(e))
            return

    # print header
    printer.set(custom_size=True, width=4, height=3)
    printer.textln(" Reparatur")
    printer.textln(" anweisung")
    printer.set()  # reset to default
    printer.ln(2)

    for instruction in instructions:
        printer.textln(instruction)
        printer.ln()
    printer.image(ASSETS_PATH / "images/combined.png", center=True)
    printer.ln()
    printer.cut()


def listen_to_serial(sentences_dict):
    ringbuffer = deque(maxlen=5)
    port = "/dev/ttyS0"
    with Serial(port, baudrate=38400, timeout=1) as ser:
        print("Listening on '" + port + "'")
        while True:
            try:
                byte = ser.read()
                ringbuffer.append(byte)
                # we expect the sequence "Print"
                if b"".join(ringbuffer).decode('utf8') == "Print":
                    instructions = generate_instructions(sentences_dict, 10)
                    print_instructions(instructions)
            except Exception as e:
                print(e)
                break


@click.option(
    "--lang",
    "-l",
    type=click.Choice(SENTENCES.keys()),
    default="de_DE",
    help="Set the language of the generated repair instructions.",
)
@click.option(
    "-n",
    default=10,
    help="Number of instructions to be created. Default: 10"
)
@click.option(
    "--quiet",
    is_flag=True,
    default=False,
    help="Do not print the sentences to STDOUT. Default: False",
)
@click.option(
    "--local_html",
    is_flag=True,
    default=False,
    help="Renders instructions into a local HTML file. Default: False"
)
@click.option(
    "--print_html",
    is_flag=True,
    default=False,
    help="Renders instructions in HTML and prints them to STDOUT. Default: False"
)
@click.option(
    "--template",
    type=click.Path(),
    default=str(DEFAULT_TEMPLATE),
    help="Specify a custom HTML template to be used.",
)
@click.option(
    "--out",
    type=click.Path(),
    default=f"static_html_content/reapair_{datetime.datetime.now().isoformat()}.html",
    help="Filename of the HTML output file.",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing HTML output file. Default: False"
)
@click.option(
    "--printer",
    is_flag=True,
    default=False,
    help="Print to the thermal printer. Default: False"
)
@click.option(
    "--listen_serial",
    is_flag=True,
    default=False,
    help="Listens to serial port 1 and prints to the thermal printer on command. Default: False"
)
@click.command()
def cli(lang, n, quiet, local_html, print_html, template, out, overwrite, printer, listen_serial):
    """
    reapAir is a tool to generate and distribute useful repair instructions for your everyday life.
    """
    try:
        sentences_dict = get_sentences(lang)
        instructions = generate_instructions(sentences_dict, n)
    except Exception as e:
        sys.exit(e)

    if listen_serial:
        listen_to_serial(sentences_dict)
        return

    if not quiet:
        for instruction in instructions:
            print(instruction)

    if printer:
        print_instructions(instructions)

    if local_html or print_html:
        html = generate_html(instructions, template)
        if print_html:
            print(html)
        if local_html:
            try:
                save_file(html, out, overwrite)
            except Exception as e:
                sys.exit(e)
