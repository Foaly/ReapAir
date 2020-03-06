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


from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent
ASSETS_PATH = BASE_PATH / "assets"
SENTENCES = {"de_DE": "sentences-de_DE.json"}
DEFAULT_TEMPLATE = ASSETS_PATH / "template.j2.html"
