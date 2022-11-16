#!/usr/bin/python

import sys

from config import *
import subprocess
import filecmp
from typing import cast
import colorama
from colorama import Style, Fore, Back



class Printer():
    current_indent: int = 0
    spaces_per_indent: int = 3
    is_print_pending: bool = False

    def colored(self, message: str, *modifiers: colorama.ansi.AnsiCodes) -> str:
        return "".join(modifiers) + message + Style.RESET_ALL

    def verbose_print(self, message: str) -> "Printer":
        if config.verbose:
            self.always_print(message)
        return self

    def always_print(self, message: str) -> "Printer":
        self.print_newline_if_pending()
        print((" " * self.current_indent * self.spaces_per_indent) + message)
        return self

    def indent(self) -> "Printer":
        self.current_indent += 1
        return self

    def deindent(self) -> "Printer":
        self.current_indent -= 1
        return self

    def print_newline_if_pending(self) -> None:
        if self.is_print_pending:
            print("")
            self.is_print_pending = False

    def start_pending_print(self, message: str) -> "Printer":
        print(message, flush=True, end="")
        self.is_print_pending = True
        return self

    def end_pending_print(self, message: str) -> "Printer":
        print(message)
        self.is_print_pending = False
        return self



printer = Printer()



class Tester():
    Result = tuple[str, int, int]

    results: list[Result] = []

    def test_all(self) -> "Tester":
        for test_dir in config.test_dirs:
            result = self.test_directory(test_dir)
            self.results.append(result)
        return self

    def test_directory(self, test_dir: str) -> Result:
        number_correct = number_total = 0

        printer.start_pending_print(
            f"Testing directory: \"{get_last_part(test_dir)}\"".ljust(45)).indent()

        in_dir = test_dir + "/in/"

        if config.keep_temp and not is_valid_path(test_dir + "/temp"):
            os.mkdir(test_dir + "/temp")

        for in_file in os.listdir(in_dir):
            is_correct = self.test_file(in_file, test_dir)

            number_total += 1
            if is_correct:
                number_correct += 1

        printer.deindent().end_pending_print(
            printer.colored((printer.colored("OK", Fore.GREEN) if number_total == number_correct
                             else printer.colored("WRONG", Fore.RED, Back.WHITE)), Style.BRIGHT))

        return (get_last_part(test_dir), number_total, number_correct)

    def test_file(self, in_file: str, test_dir: str) -> bool:
        in_last_part = in_file
        out_file = test_dir + "/out/" + in_file[:-3] + ".out"
        temp_file = (test_dir + "/temp/" + in_file[:-3]
                     + ".out" if config.keep_temp else generate_tempfile())
        in_file = test_dir + "/in/" + in_file

        if not is_valid_path(out_file):
            printer.always_print(f"File \"{in_last_part}\"".ljust(30)
                                 + printer.colored("MISSING_OUT", Fore.RED, Style.BRIGHT))
            return False

        subprocess.run(config.run_exec_cmd.format(exec=remove_blank_whitespaces(config.exec_path),
                                                  in_file=remove_blank_whitespaces(in_file),
                                                  temp_file=remove_blank_whitespaces(temp_file)),
                       shell=True)

        is_correct = self.is_correct(out_file, temp_file)

        if is_correct:
            printer.verbose_print(f"File \"{in_last_part}\"".ljust(30)
                                  + printer.colored("OK", Style.BRIGHT, Fore.GREEN))
        else:
            printer.always_print(f"File \"{in_last_part}\"".ljust(30)
                                 + printer.colored("WRONG", Style.BRIGHT, Fore.RED))

        return is_correct

    def is_correct(self, out_file: str, temp_file: str) -> bool:
        if config.is_using_custom_checker():
            return subprocess.run(config.run_custom_checker_cmd.format(
                checker=remove_blank_whitespaces(cast(str, config.custom_checker_path)),
                temp_file=remove_blank_whitespaces(temp_file)),
                                  shell=True).returncode == 0
        else:
            return filecmp.cmp(out_file, temp_file)

    def print_results(self) -> None:
        printer.always_print("Result:").indent()
        for result in self.results:
            wrong_part = "WRONG: {:>4}"
            if result[2] != result[1]:
                wrong_part = printer.colored(wrong_part, Style.BRIGHT, Back.WHITE, Fore.RED)

            printer.always_print(
                f"Test dir \"{result[0]}\"".ljust(40) +
                f"TOTAL: {result[1]:>4}   CORRECT: {result[2]:>4}   {wrong_part.format(result[1] - result[2])}"
            )



def main() -> None:
    config.parse_argv()

    tester = Tester()
    tester.test_all().print_results()



if __name__ == "__main__":
    main()
