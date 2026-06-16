VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip setuptools
	$(PIP) install -e .

run:
	$(PYTHON) sample_app/main.py

dev: install run