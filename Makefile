install:
# 	pip install --upgrade pip setuptools
	pip install -e .

run:
	python sample_app/main.py


dev: install run