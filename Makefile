install:
	pip3 install -r requirements.txt

# Run all tests
test:
	python3 -m pytest -v

# Run only a level
beginner:
	python3 -m pytest beginner/ -v

intermediate:
	python3 -m pytest intermediate/ -v

advanced:
	python3 -m pytest advanced/ -v

# Run by marker
unit:
	python3 -m pytest -m unit -v

integration:
	python3 -m pytest -m integration -v

smoke:
	python3 -m pytest -m smoke -v

fast:
	python3 -m pytest -m "not slow" -v

# Parallel execution (requires pytest-xdist)
parallel:
	python3 -m pytest -n auto -v

# Coverage for the TDD lesson
cover:
	python3 -m pytest advanced/14_tdd_coverage/ \
		--cov=advanced/14_tdd_coverage/bank_account \
		--cov-report=term-missing \
		--cov-report=html:htmlcov \
		-v

# Run with verbose output capture disabled (see print statements)
verbose:
	python3 -m pytest -v -s

# Show test durations
durations:
	python3 -m pytest --durations=10

# Run including solutions files
solutions:
	python3 -m pytest --collect-only -q | grep solution

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

.PHONY: install test beginner intermediate advanced unit integration smoke fast parallel cover verbose durations solutions clean
