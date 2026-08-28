
install:

	    pip install uv || true
		uv init || true
		uv add mypy flake8 || true
		uv sync

run:

		@clear
		@uv run python3 src/. src/configuration.json || true

debug:
# s: step into function
# n: Step Over
# r: Step Out
# l: list source code
# p: print
# q: quit
		@clear
		@uv run python -m pdb ? ? ?

uninstall:

	    uv remove ? ? ? mypy flake8

clean:
		@rm -rf src/__pycache__ .mypy_cache src/__main__.cpython*

uninstall_all: uninstall clean

		rm -rf .venv pyproject.toml uv.lock

lint:
		@clear
		uv run flake8 .  || true

		uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs || true
