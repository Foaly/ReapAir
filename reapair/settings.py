from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent
ASSETS_PATH = BASE_PATH / "assets"
SENTENCES = {"de_DE": "sentences-de_DE.txt"}
DEFAULT_TEMPLATE = ASSETS_PATH / "template.j2.html"
