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


from jinja2 import Template
import json
from .settings import ASSETS_PATH, SENTENCES


def get_template(template_path):
    """
    Checks the template file for existence, and returns a jinja2 Template
    object.
    """
    if not template_path.is_file():
        raise FileNotFoundError(f"The template file at {template_path} does not exist.")

    with open(template_path) as template_file:
        template_content = template_file.read()

    return Template(template_content)


def get_sentences(key):
    """
    Fetches the specified (i.e. language, style, category, ...) sentences
    from a json file and returns the parsed json as a dictionary.
    """
    if key not in SENTENCES.keys():
        raise ValueError(f"Sentences for {key} not found")

    sentences_path = ASSETS_PATH / SENTENCES[key]

    if not sentences_path.is_file():
        raise FileNotFoundError(
            f"The sentences file at {sentences_path} does not exist."
        )

    with open(sentences_path) as sentences_file:
        sentences_dict = json.load(sentences_file)

    return sentences_dict
