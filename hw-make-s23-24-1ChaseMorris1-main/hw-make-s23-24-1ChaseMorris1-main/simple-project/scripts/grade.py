"""
Make Homework Test Cases.
"""
import hashlib
import re
import subprocess
import unittest
from pathlib import Path
from typing import Optional, Tuple

DEBUG = False
target_pattern = re.compile(r"^(?P<targetname>.+:)")
COMMAND_FAILED_TEMPLATE = "An error occurred while trying to run '{command}'. The command's output is\n\n{output}"


class Rule:
    def __init__(
        self, targets: str | list[str], prerequisites: list[str], recipe: list[str]
    ):
        self.targets = targets
        self.prerequisites = prerequisites
        self.recipe = recipe

    @property
    def prereqs(self) -> list[str]:
        """Alias for `prerequisites`."""
        return self.prerequisites

    def __str__(self) -> str:
        targets = self.targets
        if isinstance(self.targets, list):
            targets = " ".join(self.targets)
        return f"{targets}"

    def __repr__(self) -> str:
        return str(self)

    def is_empty(self) -> bool:
        return len(self.recipe) == 0


class VariableDefinition:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class Makefile:
    def __init__(
        self,
        path: Path | str,
        variable_definitions: list[VariableDefinition],
        rules: list[Rule],
    ):
        self.path = path
        self.variable_definitions = variable_definitions
        self.rules = rules

    @classmethod
    def from_path(cls, path: Path | str):
        with open(path, "r") as f:
            var_defs: list[VariableDefinition] = []
            rules: list[Rule] = []

            lines = f.readlines()
            current_rule: Optional[Rule] = None
            for line in lines:
                line = line.strip()

                if DEBUG:
                    print(f"parsing '{line}'")

                if len(line) != 0:
                    if line[0] == "#":
                        continue

                    if line[0] != "\t" and ":" in line:
                        if DEBUG:
                            print("line is the begining of a rule")
                        if current_rule is not None:
                            rules.append(current_rule)

                        target_token, prerequisite_token = line.split(":")
                        if " " in target_token:
                            targets = target_token.split(" ")
                        else:
                            targets = target_token

                        prereqs = [
                            t.strip()
                            for t in prerequisite_token.split(" ")
                            if len(t.strip()) != 0
                        ]
                        current_rule = Rule(
                            targets=targets, prerequisites=prereqs, recipe=list()
                        )
                    elif line[0] != "\t" and "=" in line:
                        if DEBUG:
                            print("line is a variable definition")
                        # Only act on the first '='.
                        equal_pos = line.find("=")
                        name = line[:equal_pos]
                        value = line[equal_pos+1:]

                        var_defs.append(
                            VariableDefinition(name=name.strip(), value=value.strip())
                        )
                    else:
                        if DEBUG:
                            print("line is part of the recipe")
                        current_rule.recipe.append(line[1:])
                else:
                    if current_rule is not None:
                        rules.append(current_rule)
                        current_rule = None

            if current_rule is not None:
                rules.append(current_rule)
            return cls(path, var_defs, rules)

    def get_rule(self, targets: str | list[str]) -> Optional[Rule]:
        for rule in self.rules:
            if rule.targets == targets:
                return rule

        return None

    def has_rule(self, targets: str | list[str]) -> bool:
        rule = self.get_rule(targets)
        return rule is not None


def run_executable(args, cwd: Optional[str | Path] = None) -> Tuple[bool, str]:
    try:
        make_cmd_output = subprocess.check_output(
            args, stderr=subprocess.STDOUT, cwd=cwd
        )
        return True, make_cmd_output.decode()
    except subprocess.CalledProcessError as e:
        return False, e.output.decode()


def run_targets(
    targets: list[str], cwd: Optional[str | Path] = None
) -> Tuple[bool, str]:
    """
    Invoke the target(s) in the Makefile.

    Return True if the call is successful, False otherwise.
    Also return the output of the executation.
    """
    return run_executable(["make"] + targets, cwd=cwd)


def has_file(filepath: Path | str) -> bool:
    if isinstance(filepath, str):
        filepath = Path(filepath)
    return filepath.exists()


def has_files(filepaths: list[Path] | list[str]) -> bool:
    """Return True if all listed file exist."""
    return all([has_file(p) for p in filepaths])


def archive_contain_files(archive_filepath: Path | str, files: list[str]) -> bool:
    return False


def remove_file(filepath: Path | str):
    if isinstance(filepath, str):
        filepath = Path(filepath)
    filepath.unlink(missing_ok=True)


def test_file_hash():
    with open("test_cases.py", "rb") as f:
        data = f.read()
        hash_val = hashlib.sha256(data).hexdigest()
        print(hash_val)


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


class MakefileBaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not hasattr(cls, "makefile_name"):
            raise AttributeError("'makefile_name' is required")

        if isinstance(cls.makefile_name, str):
            cls.makefile_name = Path(cls.makefile_name)

        if not cls.makefile_name.exists():
            assert False, f"Expect a file '{cls.makefile_name}', but it does not exist."

        cls.makefile = Makefile.from_path(cls.makefile_name)


class TestAllRuleBehavior(MakefileBaseTestCase):
    makefile_name = Path("source") / "Makefile"

    def test_all_rule_behavior(self):
        """
        Behavior of a rule for a target 'all'.

        'all' should be the goal target. When it is invoked, the executable files and the
        source distribution archive file are created. The recipe of this target must be empty.
        """
        rule = self.makefile.get_rule("all")
        assert (
            rule is not None
        ), "Rule for a target 'all' does not exist. Its behavior cannot be verified."
        assert rule.is_empty(), "Recipe of the rule for a target 'all' is not empty."

        #
        # Remove any existing file.
        #
        remove_file(Path("source") / "othello-game")
        remove_file(Path("source") / "othello-game-debug")
        remove_file(Path("source") / "othello-sdist.tar.gz")

        is_success, output = run_targets([], cwd=Path("source"))
        assert is_success, COMMAND_FAILED_TEMPLATE.format(
            command="make all", output=output
        )

        description = "one or more of the expected files ('othello-game', 'othello-game-debug', 'othello-sdist.tar.gz') does not exist after the make command is run."
        assert has_files(
            [
                Path("source") / "othello-game",
                Path("source") / "othello-game-debug",
                Path("source") / "othello-sdist.tar.gz",
            ]
        ), description

        #
        # Check if the executables are working.
        #
        is_success, output = run_executable(
            ["./othello-game", "--version"], cwd=Path("source")
        )
        assert is_success, COMMAND_FAILED_TEMPLATE.format(
            command="./othello-game --version", output=output
        )
        assert (
            output == "2024.1\n"
        ), f"Output of './othello-game --version' is not as expected. Output of the command is\n\n{output}"

        is_success, output = run_executable(
            ["./othello-game-debug", "--version"], cwd=Path("source")
        )
        assert is_success, COMMAND_FAILED_TEMPLATE.format(
            command="./othello-game-debug --version", output=output
        )
        assert (
            output == "2024.1d\n"
        ), f"Output of './othello-game-debug --version' is not as expected. Output of the command is\n\n{output}"

    def tearDown(self):
        remove_file(Path("source") / "othello-game")
        remove_file(Path("source") / "othello-game-debug")
        remove_file(Path("source") / "othello-sdist.tar.gz")


class TestBuildRelatedTargetBehavior(MakefileBaseTestCase):
    makefile_name = Path("source") / "Makefile"

    def test_build_behavior(self):
        """
        Behavior of target 'build'
        """
        #
        # Only check the target behavior when the target actually exist.
        #
        rule = self.makefile.get_rule("build")
        assert (
            rule is not None
        ), "Rule for target 'build' does not exist. Its behavior cannot be verified."
        assert rule.is_empty(), "Rule for target build is not empty."

        #
        # Remove any existing file.
        #
        remove_file(Path("source") / "othello-game")
        remove_file(Path("source") / "othello-game-debug")

        #
        # Running `make build`
        #
        is_success, output = run_targets(["build"], cwd=Path("source"))
        assert is_success, COMMAND_FAILED_TEMPLATE.format(
            command="make build", output=output
        )
        description = "one or more of the expected files ('othello-game', 'othello-game-debug') does not exist after the make command is run."
        assert has_files(
            [Path("source") / "othello-game", Path("source") / "othello-game-debug"]
        ), description

        #
        # Double invocation does not create the file again.
        #
        success, make_cmd_output = run_targets(["build"], cwd=Path("source"))
        assert (
            "make: Nothing to be done for 'build'." in make_cmd_output
        ), "Rule for the target 'build' appears to create at least one of the executables again when nothing has changed."

        #
        # Check if the executables are working.
        #
        is_success, output = run_executable(
            ["./othello-game", "--version"], cwd=Path("source")
        )
        assert is_success, COMMAND_FAILED_TEMPLATE.format(
            command="./othello-game --version", output=output
        )
        assert (
            output == "2024.1\n"
        ), f"Output of './othello-game --version' is not as expected. Output of the command is\n\n{output}"

        is_success, output = run_executable(
            ["./othello-game-debug", "--version"], cwd=Path("source")
        )
        assert is_success, COMMAND_FAILED_TEMPLATE.format(
            command="./othello-game-debug --version", output=output
        )
        assert (
            output == "2024.1d\n"
        ), f"Output of './othello-game-debug --version' is not as expected. Output of the command is\n\n{output}"

    def tearDown(self):
        remove_file(Path("source") / "othello-game")
        remove_file(Path("source") / "othello-game-debug")


class TestSdistTargetBehavior(MakefileBaseTestCase):
    makefile_name = Path("source") / "Makefile"

    def test_sdist_behavior(self):
        """Behavior of target 'sdist'"""
        #
        # Only check the target behavior when the target actually exist.
        #
        if not self.makefile.has_rule("sdist"):
            assert (
                False
            ), "Rule for target 'sdist' do not exist. Its behavior cannot be verified."

        expected_filepath = Path("source") / "othello-sdist.tar.gz"

        # Removing any existing othello-sdist.tar.gz.
        remove_file(expected_filepath)

        #
        # othello-sdist.tar.gz is created.
        #
        success, output = run_targets(["sdist"], cwd=Path("source"))
        assert success, COMMAND_FAILED_TEMPLATE.format(
            command="make sdist", output=output
        )
        assert (
            expected_filepath.exists()
        ), "Rule for the target 'sdist' does not create the expected file named 'othello-sdist.tar.gz'."

        #
        # Double invocation does not create the file again.
        #
        success, make_cmd_output = run_targets(["sdist"], cwd=Path("source"))
        assert (
            "make: Nothing to be done for 'sdist'." in make_cmd_output
        ), "Rule for the target 'sdist' appears to create 'othello-sdist.tar.gz' again when nothing has changed."

        #
        # Check content of othello-sdist.tar.gz
        #
        expected_files_in_archive = [
            "colors.hpp",
            "debug_main.cpp",
            "game.cpp",
            "game.hpp",
            "main.cpp",
            "Makefile",
            "othello.cpp",
            "othello.hpp",
            "piece.hpp",
        ]
        is_success, output = run_executable(["tar", "-tf", expected_filepath])
        assert is_success, COMMAND_FAILED_TEMPLATE.format(
            command=f"tar -tf {str(expected_filepath)}", output=output
        )
        lines = output.split("\n")
        for expected_file in expected_files_in_archive:
            assert (
                expected_file in lines
            ), f"File '{expected_file}' is not in the othello-sdist.tar.gz"


class TestCleanTargetBehavior(MakefileBaseTestCase):
    makefile_name = Path("source") / "Makefile"
    files_expected_to_be_clean = [
        "game.o",
        "othello.o",
        "main.o",
        "debug_main.o",
        "othello-game",
        "othello-game-debug",
    ]

    def tearDown(self):
        for f in [Path("source") / f for f in self.files_expected_to_be_clean]:
            if f.exists():
                f.unlink()

    def test_clean_object_files_behavior(self):
        """
        Behavior of the rule for target 'clean'

        Running the command "make clean" should remove all the .o files
        and the executable file.

        Note: The executable file is not detected yet since the name can be arbitrary.
        """
        # Only check the target behavior when the target actually exist.
        if not self.makefile.has_rule("clean"):
            assert False, "Target does not exist. Its behavior cannot be verified."

        # Manually create .o file.
        for obj_f in self.files_expected_to_be_clean:
            with open(Path("source") / obj_f, "w") as f:
                f.write("object-file; created by the test cases")

        # Run the `make clean`
        success, output = run_targets(["clean"], cwd=Path("source"))
        assert success, COMMAND_FAILED_TEMPLATE.format(
            command="make clean", output=output
        )
        assert "error" not in output, COMMAND_FAILED_TEMPLATE.format(
            command="make clean", output=output
        )

        #
        # All required files should be deleted.
        #
        files = list(Path("source").glob("./*.o"))
        files_text = "\n".join(str(f) for f in files)
        assert (
            len(files) == 0
        ), f"'make clean' does not remove all expected .o files.\n\n{files_text}"


if __name__ == "__main__":
    runner = unittest.TextTestRunner(resultclass=MinimalistTestResult)
    unittest.main(testRunner=runner)
