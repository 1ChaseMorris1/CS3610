"""Rough Makefile Linter.

This linter target common problems that occur in this homework.
Namely the space is used to start the command portion of the
target.

The linter does not perform a context aware check and will
suggest that any space that is leading a line is an error.
"""

from pathlib import Path
import functools

VALIDATORS = []


def validator(func):
    """Add the function to VALIDATORS list."""
    VALIDATORS.append(func)

    @functools.wraps(func)
    def identity(*args, **kwargs):
        return func(*args, **kwargs)

    return identity


@validator
def line_should_start_with_tab(lines: list[str]):
    for idx, line in enumerate(lines, start=1):
        if line[0] == " ":
            print(f"Line {idx} of the Makefile started with space(s).")
            print("Do you mean to use tab? GNU Make only work with tab")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="A path to the Makefile")

    args = parser.parse_args()

    path = Path(args.filepath)

    if path.exists() and path.is_file():
        with open(path) as f:
            lines = f.readlines()

            for v in VALIDATORS:
                v(lines)
    else:
        print(f"Cannot find a file '{str(path)}'")
