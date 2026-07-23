VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install  --verbose --upgrade pip setuptools
	$(PIP) install --verbose -e .

run:
	$(PYTHON) sample_app/main.py

dev: install run


clean:
	$(PYTHON) -c "import shutil, os; [shutil.rmtree(p, ignore_errors=True) for p in ('$(VENV)', 'syringe.egg-info', '.pytest_cache', '__pycache__', 'syringe/__pycache__')];"
