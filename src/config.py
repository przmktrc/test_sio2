import sys

import os
import PyArg
import re
import subprocess
from typing import Optional, cast
from print_help import print_help



class InvalidConfig(RuntimeError):
    def __init__(self, reason: str = "") -> None:
        if reason == "":
            super().__init__("Run with --help for more information.")
        else:
            super().__init__(f"{reason}. Run with --help for more information.")



def remove_blank_whitespaces(path: str | list[str]) -> str | list[str]:
    if isinstance(path, list):
        return [cast(str, remove_blank_whitespaces(cast(str, single_path))) for single_path in path]
    else:
        return re.sub(r" ", r"\ ", path)



def is_valid_path(path: str) -> bool:
    return os.path.exists(path)



def get_last_part(path: str) -> str:
    return path.split("/")[-1]



def generate_tempfile() -> str:
    return subprocess.run("mktemp", capture_output=True, text=True).stdout[:-1]



class Config():
    run_exec_cmd: str = "{exec} < {in_file} > {temp_file}"
    run_custom_checker_cmd: str = "{checker} < {temp_file}"

    keep_temp: bool = True
    verbose: bool = False
    exec_path: str = ""
    was_help_printed: bool = False
    custom_checker_path: Optional[str] = None
    test_dirs: list[str] = []

    parser: PyArg.ArgParser

    def __init__(self) -> None:
        self.parser = PyArg.ArgParser(arg_actors=[
            (["-v", "--verbose"], self.set_verbose),
            ("--notemp", self.set_nokeep_temp),
            (["-e", "--exec"], self.set_exec),
            ("--checker", self.set_custom_checker),
            (["-h", "--help"], self.print_help),
        ],
                                      default_arg_actor=self.add_test_dir)

    def set_verbose(self, _1, _2) -> None:
        self.verbose = True

    def set_nokeep_temp(self, _1, _2) -> None:
        self.keep_temp = False

    def set_exec(self, _1, parser: PyArg.ArgParser) -> None:
        to_set = os.getcwd() + "/" + parser.get_next_arg()
        if is_valid_path(to_set):
            self.exec_path = to_set
        else:
            raise InvalidConfig(f"Invalid executable path: \"{to_set}\"")

    def set_custom_checker(self, _1, parser: PyArg.ArgParser) -> None:
        to_set = os.getcwd() + "/" + parser.get_next_arg()
        if is_valid_path(to_set):
            self.custom_checker_path = to_set
        else:
            raise InvalidConfig(f"Invalid checker path: \"{to_set}\"")

    def print_help(self, _1, _2) -> None:
        print_help()
        self.was_help_printed = True

    def add_test_dir(self, dir: str, _2) -> None:
        if dir == "": return

        to_add = os.getcwd() + "/" + dir
        if is_valid_path(to_add):
            self.test_dirs.append(to_add)
        else:
            raise InvalidConfig(f"Invalid test dir: \"{to_add}\"")

    def parse_argv(self, argv: list[str] = sys.argv[1:]) -> None:
        self.reset()
        self.parser.parse(argv)

    def reset(self) -> None:
        self.keep_temp = True
        self.verbose = False
        self.exec_path = ""
        self.custom_checker_path = None
        self.test_dirs = []

    def is_using_custom_checker(self) -> bool:
        return self.custom_checker_path != None

    def validate(self) -> None:
        if self.exec_path == "":
            raise InvalidConfig("Executable path not specified")

        if self.test_dirs == []:
            raise InvalidConfig("No test dir specified")



config = Config()
