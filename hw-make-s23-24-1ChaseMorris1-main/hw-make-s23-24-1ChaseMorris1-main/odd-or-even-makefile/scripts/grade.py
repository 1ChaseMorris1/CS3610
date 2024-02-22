import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

DEBUG = False
FILE_NAME_TEMPLATE = "{}.txt"
MIN_AMOUNT = 1
MAX_AMOUNT = 20


def populate_folder(path: Path | str, is_even: bool) -> int:
    """
    Randomly populates the folder data folder full of files.

    Return the amount of files populated.
    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ValueError("'path' does not exist")

    if not path.is_dir():
        raise ValueError("'path' is not a directory")

    if is_even:
        choices = [v for v in range(MIN_AMOUNT, MAX_AMOUNT) if v % 2 == 0]
    else:
        choices = [v for v in range(MIN_AMOUNT, MAX_AMOUNT) if v % 2 == 1]

    amount = random.choice(choices)
    for idx in range(amount):
        with open(path / FILE_NAME_TEMPLATE.format(idx), "w") as f:
            f.write("")

    return amount


def grade(is_even: bool):
    with tempfile.TemporaryDirectory(dir=Path("."), delete=not DEBUG) as tmpdirname:
        path = Path(tmpdirname)
        data_root = path / "data"
        data_root.mkdir()

        amount = populate_folder(data_root, is_even)
        shutil.copy(Path("Makefile"), path / "Makefile")

        if is_even:
            print("[grade]: testing the Makefile with a test case (even) ... ", end="")
        else:
            print("[grade]: testing the Makefile with a test case (odd) ... ", end="")

        output = subprocess.check_output(f"make", cwd=str(path), shell=True)
        if output is None:
            print("fail")
            sys.exit(1)
        else:
            output = output.decode()
            if DEBUG:
                print(f"[debug]: {amount=}")
                print(f"[debug]: output from make command '{output}'")

            if amount % 2 == 0 and output == "even\n":
                print("pass")
                sys.exit(0)
            elif amount % 2 == 1 and output == "odd\n":
                print("pass")
                sys.exit(0)
            else:
                print("fail")
                sys.exit(2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=int(time.time()))
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("type", choices=("even", "odd"))
    args = parser.parse_args()

    print(f"seed: {args.seed}")
    random.seed(args.seed)

    if args.debug:
        DEBUG = True

    python_version = (sys.version_info.major, sys.version_info.minor)

    if python_version < (3, 12):
        print("[error]: the script requires Python version >= 3.12")
        sys.exit()

    if args.type == "even":
        grade(is_even=True)
    elif args.type == "odd":
        grade(is_even=False)
