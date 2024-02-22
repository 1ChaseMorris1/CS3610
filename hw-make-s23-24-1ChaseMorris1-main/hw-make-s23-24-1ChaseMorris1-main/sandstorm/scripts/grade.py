import sys
import subprocess
from time import sleep


def check_active_sandstorm():
    subprocess.run("touch sandstorm.txt", shell=True)
    sleep(0.2)

    try:
        output = subprocess.check_output(
            "make --silent", stderr=subprocess.STDOUT, shell=True
        )

        if output is None:
            print("[grade]: checking Makefile when sandstorm is active ... fail")
            print("    no output from running the command 'make --silent'")
            sys.exit(2)
        elif output.decode() == "warning, a sandstorm is active!\n":
            print("[grade]: checking Makefile when sandstorm is active ... pass")
            sys.exit(0)
        else:
            print("[grade]: checking Makefile when sandstorm is active ... fail")
            sys.exit(2)
    except subprocess.CalledProcessError as e:
        print("[grade]: checking Makefile when sandstorm is active ... error")
        print(f"    content in stdout and stderr from command '{e.cmd}':", end="\n\n")
        print("", e.stdout.decode(), sep="    ")
        sys.exit(1)


def check_inactive_sandstorm():
    subprocess.run("touch calm.txt", shell=True)
    sleep(0.2)

    try:
        output = subprocess.check_output(
            "make --silent", stderr=subprocess.STDOUT, shell=True
        )
        if output is None:
            print("[grade]: checking Makefile when sandstorm is NOT active ... fail")
            sys.exit(2)
        elif output.decode() == "":
            print("[grade]: checking Makefile when sandstorm is NOT active ... pass")
            sys.exit(0)
        else:
            print("[grade]: checking Makefile when sandstorm is NOT active ... fail")
            sys.exit(2)
    except subprocess.CalledProcessError as e:
        print("[grade]: checking Makefile when sandstorm is active ... error")
        print(f"    content in stdout and stderr from command '{e.cmd}':", end="\n\n")
        print("", e.stdout.decode(), sep="    ")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "active":
            check_active_sandstorm()
        elif sys.argv[1] == "inactive":
            check_inactive_sandstorm()
    else:
        check_active_sandstorm()
        check_inactive_sandstorm()
