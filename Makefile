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


.DEFAULT_GOAL := help

.PHONY: help
help:
    @grep -E '^[\.a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: black
black: ## Format the code
    python -m black reapair

.PHONY: flake
flake: ## Flake8 the code
    flake8 --max-line-length=99 reapair

.PHONY: check
check: flake ## Perform black and flake checks (Should be done pre-commit)
    python -m black --check reapair
