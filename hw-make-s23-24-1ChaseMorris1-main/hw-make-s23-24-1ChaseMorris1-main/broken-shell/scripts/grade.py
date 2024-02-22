"""
A script that grade this problem.

Steps:
1. Make a copy of the student Makefile to `answer.mk`
2. In this new Makefile, overwrite the `SHELL` variable with our `shell.py`
3. Run `make -f answer.mk` in the source folder.
"""
import unittest
from pathlib import Path
import subprocess


class TestLimitedResourcesPuzzle(unittest.TestCase):
    def test_makefile(self):
        student_makefile_path = Path("source") / "Makefile"
        our_makefile_path = Path("source") / "answer.mk"

        if not student_makefile_path.exists():
            assert False, "Makefile not found in source folder."

        # Copy the student Makefile to answer.mk
        with open(student_makefile_path, "r") as in_f:
            lines = in_f.readlines()

            lines = ["SHELL=../scripts/shell.py\n"] + lines

            with open(our_makefile_path, "w") as out_f:
                for line in lines:
                    out_f.write(line)

        # Run make
        try:
            expected_executable_filepath = Path("source") / "money-printer"
            make_cmd_output = subprocess.check_output(["make", "-f", "answer.mk"], cwd=Path("source"), stderr=subprocess.STDOUT).decode()
            assert expected_executable_filepath.exists(), "Executable not found."
        except subprocess.CalledProcessError as e:
            assert False, f"Make command ('{e.cmd}') failed with output:\n\n{e.output.decode()}"

    def tearDown(self) -> None:
        # Clean up the executable
        executable_path = Path("source") / "money-printer"
        if executable_path.exists():
            executable_path.unlink()

        # Clean up the answer.mk
        our_makefile_path = Path("source") / "answer.mk"
        if our_makefile_path.exists():
            our_makefile_path.unlink()


class MinimalistTestResult(unittest.TextTestResult):
    """TextTestResult without the traceback.

    Traceback is too verbose for our purpose.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dots = False

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return doc_first_line
        else:
            return str(test)

    def addFailure(self, test, err):
        self.failures.append((test, str(err[1]) + "\n"))
        self._mirrorOutput = True

        if self.showAll:
            self._write_status(test, "FAIL")
        elif self.dots:
            self.stream.write("F")
            self.stream.flush()


if __name__ == "__main__":
    runner = unittest.TextTestRunner(resultclass=MinimalistTestResult)
    unittest.main(testRunner=runner)
