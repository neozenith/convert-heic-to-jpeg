init:
	[ ! -d ".venv" ] && python3 -m venv .venv || echo ".venv already setup"
	.venv/bin/python3 -m pip install -qq --upgrade pip
	.venv/bin/python3 -m pip install -qq --upgrade wheel pip-tools pre-commit
	.venv/bin/pre-commit install

lock:
	.venv/bin/python3 -m piptools compile --generate-hashes --upgrade --resolver backtracking -o requirements.txt pyproject.toml
	.venv/bin/python3 -m piptools compile --extra dev --upgrade --resolver backtracking -o requirements-dev.txt pyproject.toml

prod:
	.venv/bin/python3 -m pip install \
    	--require-hashes --no-deps \
    	-r requirements.txt
	.venv/bin/python3 -m pip install .  # <- the app/pkg itself

dev:
	.venv/bin/python3 -m pip install \
    	-r requirements-dev.txt \
    	--editable .  # <- the app/pkg itself

run:
	.venv/bin/python3 -m idp_fuel_tracker

docs:
	.venv/bin/md_toc --in-place github --header-levels 4 README.md


fix:
	.venv/bin/ruff check . --fix
	.venv/bin/pre-commit run
	.venv/bin/isort .

all: init lock dev fix run