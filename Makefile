install:
# 	pip install --upgrade pip setuptools
	pip install -e .

run:
	python my_app/main.py


dev: install run