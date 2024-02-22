#!/usr/bin/env python3
"""
A broken shell.

This shell will refuse to run any command that
- is longer than 60 characters.
- contains an asterisk.
"""
import sys
import subprocess

DEBUG = True
MAX_COMMAND_LENGTH = 60

def contain_an_asterisk(cmd: str) -> bool:
    return "*" in cmd


def is_with_length(cmd: str) -> bool:
    if (cmd[0] == '"' and cmd[-1] == '"') or (cmd[0] == "'" and cmd[-1] == "'"):
        # Remove the quotes.
        cmd = cmd[1:-1]

    tokens = [token.strip() for token in cmd.split(" ")]
    tokens = [token for token in tokens if len(token) != 0]

    processed_cmd = " ".join(tokens)
    if DEBUG:
        print(f"command: '{processed_cmd}'")
        print(f"command's length = {len(processed_cmd)}")

    if len(processed_cmd) <= MAX_COMMAND_LENGTH:
        return True
    return False


def count_cpp_source_files(cmd: str) -> int:
    tokens = [token.strip() for token in cmd.split(" ")]
    count = sum([1 for token in tokens if token.endswith("cpp") or token.endswith("cc")])
    return count

def main(argv):
    cmd = argv[2]
    if count_cpp_source_files(cmd) > 1:
        print(
            f"[a-broken-shell]: The command '{cmd}' has more than one C++ source file",
            file=sys.stderr,
        )
        sys.exit(1)
    elif contain_an_asterisk(cmd):
        print(
            f"[a-broken-shell]: Cannot run a command containing an asterisk.",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        subprocess.run(["/bin/bash"] + argv[1:])


if __name__ == "__main__":
    main(sys.argv)
