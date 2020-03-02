from jinja2 import Template
from pathlib import Path
from .settings import ASSETS_PATH, SENTENCES

def get_template(template_path):
    """
    Checks the template file for existence, and returns a jinja2 Template
    object.
    """
    if not template_path.is_file():
        raise FileNotFoundError(
            f"The template file at {template_path} does not exist."
        )

    with open(template_path) as template_file:
        template_content = template_file.read()

    return Template(template_content)

def get_sentences(key, strip_comments="#", strip_empty=True):
    """
    Fetches the specified (i.e. language, style, category, ...) sentences
    from a file and returnes a list of these.

    strip_comments (optional) string: If False (or empty string),
    this setting is ignored. If set, lines starting with the given string
    will not be in the final result.

    strip_empty (optional) bool: If True, empty lines will not appear in the
    final result.
    """
    if not key in SENTENCES.keys():
        raise ValueError(f"Sentences for {key} not found")

    sentences_path = ASSETS_PATH / SENTENCES[key]

    if not sentences_path.is_file():
        raise FileNotFoundError(
            f"The sentences file at {sentences_path} does not exist."
        )

    with open(sentences_path) as sentences_file:
        lines = sentences_file.readlines()

    sentences = []
    for line in lines:
        if strip_comments:
            if line.startswith(strip_comments):
                continue
        stripped = line.strip()

        if strip_empty:
            if not len(stripped):
                continue

        sentences.append(stripped)

    return sentences
