ReapAir
========

<p align="center">
  <img width="100%" src="assets/reapAir.png">
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

## Usage

The installation gives you a shell command **reapair** which can be executed from anywhere.

```zsh
$ reapAir --help

Usage: reapAir [OPTIONS]

  reapAir is a tool to generate and distribute useful repair instructions
  for your everyday life.

Options:
  --overwrite TEXT    Overwrite existing HTML output file.
  --out TEXT          Filename of the HTML output file.
  --template PATH     Specify a custom HTML template to be used.
  --html              Render HTML output. Default: False
  --quiet             Do not print the sentences to STDOUT. Default: False
  -n INTEGER          Number of instructions to be created.
  -l, --lang [de_DE]  Set the language of the generated repair instructions.
  --help              Show this message and exit.
```

## Examples

Generate 15 sentences and print them to STDOUT

```zsh
$ reapAir -n 15
```

Generate 10 sentences (default) and create a html file named *example-010.html* and use a custom HTML template named *template.html*. Furthermore suppress output on STDOUT.

```zsh
$ reapAir --html --out example-010.html --template template.html --quiet
```

## Authors

* Foaly
* olf42
