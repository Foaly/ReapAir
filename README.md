ReapAir
========

<p align="center">
  <img width="100%" src="reapair/assets/images/reapAir_logo.png">
</p>

Work less, support more.

**ReapAir** is a tool to generate and distribute useful repair instructions for your everyday life.

## Installation

You can either install this application systemwide, in a virtual environment (e.g. virtualenv/venv/pipenv) or for the user.

### Systemwide / Virtual environment installation

First, you (optionally) create a venv and activate it.

```zsh
$ python3 -m venv ./PATH_TO_VENV
$ source ./PATH_TO_VENV/bin/activate
```

Then you install the latest version from github:

```zsh
$ pip install git+https://github.com/Foaly/ReapAir
```

### User installation

```zsh
$ pip install --user git+https://github.com/Foaly/ReapAir
```

### Development installation

```zsh
$ git clone git@github.com:Foaly/ReapAir.git
$ python3 -m venv ./PATH_TO_VENV
$ source ./PATH_TO_VENV/bin/activate
$ pip install poetry
$ poetry install
```

## Usage

The installation gives you a shell command **reapair** which can be executed from anywhere.

```zsh
$ reapAir --help

Usage: reapAir [OPTIONS]

  reapAir is a tool to generate and distribute useful repair instructions
  for your everyday life.

Options:
  --listen_serial     Listens to serial port 1 and prints to the thermal
                      printer on command. Default: False

  --printer           Print to the thermal printer. Default: False
  --overwrite         Overwrite existing HTML output file. Default: False
  --out PATH          Filename of the HTML output file.
  --template PATH     Specify a custom HTML template to be used.
  --print_html        Renders instructions in HTML and prints them to STDOUT.
                      Default: False

  --local_html        Renders instructions into a local HTML file. Default:
                      False

  --quiet             Do not print the sentences to STDOUT. Default: False
  -n INTEGER          Number of instructions to be created. Default: 10
  -l, --lang [de_DE]  Set the language of the generated repair instructions.
  --help              Show this message and exit.
```

## Examples

Generate 15 sentences and print them to STDOUT.

```zsh
$ reapAir -n 15
```

Generate 10 sentences (default) and create a html file named *example-010.html* and use a custom HTML template named *template.html*. Furthermore suppress output on STDOUT.

```zsh
$ reapAir --html --out example-010.html --template template.html --quiet
```

Print 15 sentences to the attached thermal printer, but not to STDOUT.

```zsh
reapAir --quiet --printer -n 15
```

## Authors

* Foaly
* olf42

## License

All code in this repository is licensed under the GPLv3.
For more details refer to [`LICENSE.md`](./LICENSE.md).
