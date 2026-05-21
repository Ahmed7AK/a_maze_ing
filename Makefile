PYTHON = python3
PROGRAM = a_maze_ing.py
CONFIG = config.txt
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

install: ;

run:
	$(PYTHON) $(PROGRAM) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(PROGRAM) $(CONFIG)

clean:
	rm -rf ./__pycache__ ./mazegen/__pycache__ ./.mypy_cache

lint:
	-flake8 .
	-$(PYTHON) -m mypy . $(MYPY_FLAGS)