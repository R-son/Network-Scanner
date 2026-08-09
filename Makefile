PYTHON = python3

PROGRAM = main.py
TEST_DIR = tests

.PHONY: help run test test-verbose check clean

help:
	@echo "Network Scanner"
	@echo ""
	@echo "Available targets:"
	@echo "  make run                         Run the scanner"
	@echo "  make run ARGS=\"--ip 127.0.0.1\" Run scanner with arguments"
	@echo "  make test                        Run unit tests"
	@echo "  make test-verbose                Run unit tests with verbose output"
	@echo "  make check                       Run tests and Python syntax checks"
	@echo "  make clean                       Remove Python cache files"

run:
	$(PYTHON) $(PROGRAM) $(ARGS)

test:
	$(PYTHON) -m unittest discover -s $(TEST_DIR)

test-verbose:
	$(PYTHON) -m unittest discover -s $(TEST_DIR) -v

check:
	$(PYTHON) -m compileall -q .
	$(PYTHON) -m unittest discover -s $(TEST_DIR) -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete