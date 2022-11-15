import sys

sys.path.append("../")

import os
import PyArg
import re
from typing import Optional, cast



class InvalidConfig(RuntimeError):
    def __init__(self, reason: str = "") -> None:
        if reason == "":
            super().__init__("Run with --help for more information.")
        else:
            super().__init__("{}. Run with --help for more information.".format(reason))



def remove_blank_whitespaces(path: str | list[str]) -> str | list[str]:
    if isinstance(path, list):
        return [cast(str, remove_blank_whitespaces(cast(str, single_path))) for single_path in path]
    else:
        return re.sub(r" ", r"\ ", path)



def is_valid_path(path: str) -> bool:
    return os.path.exists(path)



class Config():
    keep_temp: bool = True
    verbose: bool = False
    exec_path: str = ""
    custom_checker_path: Optional[str] = None
    test_dirs: list[str] = []

    parser: PyArg.ArgParser

    def __init__(self) -> None:
        self.parser = PyArg.ArgParser(arg_actors=[
            (["-v", "--verbose"], self.set_verbose),
            ("--notemp", self.set_nokeep_temp),
            (["-e", "--exec"], self.set_exec),
            ("--checker", self.set_custom_checker),
        ],
                                      default_arg_actor=self.add_test_dir)

    def set_verbose(self, _1, _2) -> None:
        self.verbose = True

    def set_nokeep_temp(self, _1, _2) -> None:
        self.keep_temp = False

    def set_exec(self, _1, parser: PyArg.ArgParser) -> None:
        self.exec_path = os.getcwd() + "/" + parser.get_next_arg()
        if not is_valid_path(self.exec_path):
            raise InvalidConfig("Invalid executable path: \"{}\"".format(self.exec_path))

    def set_custom_checker(self, _1, parser: PyArg.ArgParser) -> None:
        self.custom_checker_path = os.getcwd() + "/" + parser.get_next_arg()
        if not is_valid_path(self.custom_checker_path):
            raise InvalidConfig("Invalid checker path: \"{}\"".format(self.custom_checker_path))

    def add_test_dir(self, dir: str, _2) -> None:
        if dir == "": return

        self.test_dirs.append(os.getcwd() + "/" + dir)
        if not is_valid_path(self.test_dirs[-1]):
            raise InvalidConfig("Invalid test dir: \"{}\"".format(self.test_dirs[-1]))

    def parse_argv(self, argv: list[str] = sys.argv[1:]) -> None:
        self.reset()
        self.parser.parse(argv)

    def reset(self) -> None:
        self.keep_temp = True
        self.verbose = False
        self.exec_path = ""
        self.custom_checker_path = None
        self.test_dirs = []



config = Config()