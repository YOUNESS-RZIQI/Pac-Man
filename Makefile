
install:

	    pip install uv || true
		uv init || true
		uv add ? ? ? mypy flake8 || true
		uv sync

run:

		@clear
		@uv run ? ? ? || true

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
		@rm -rf __pycache__ .mypy_cache

uninstall_all: uninstall clean

		rm -rf .venv/

lint:
		@clear
		uv run flake8 .  || true

		uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs || true
