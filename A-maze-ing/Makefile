
PY = python3
MAIN = a_maze_ing.py
CONFG = config.txt


install:
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install --upgrade poetry
	$(PY) -m pip install flake8
	$(PY) -m pip install pydantic
	$(PY) -m pip install pydantic_settings
	$(PY) -m pip install mypy
	$(PY) -m pip install wheel
	$(PY) -m pip install setuptools
	clear

run:
	$(PY) $(MAIN) $(CONFG)


debug:
	$(PY) -m pdb $(MAIN) $(CONFG)


clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .mypy_cache
	rm -f *.pyc */*.pyc */*/*.pyc

lint:
	python3 -m flake8 . || true
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs || true


.PHONY: install run debug clean lint