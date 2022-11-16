#!/usr/bin/python

import sys

from config import *
import subprocess
import filecmp
from typing import cast



def verbose_print(message: str) -> None:
    if config.verbose:
        print(message)



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

        print("Testing directory: \"{}\"".format(get_last_part(test_dir)))

        in_dir = test_dir + "/in/"

        if config.keep_temp and not is_valid_path(test_dir + "/temp"):
            os.mkdir(test_dir + "/temp")

        for in_file in os.listdir(in_dir):
            is_correct = self.test_file(in_file, test_dir)

            number_total += 1
            if is_correct:
                number_correct += 1

        return (get_last_part(test_dir), number_total, number_correct)

    def test_file(self, in_file: str, test_dir: str) -> bool:
        out_file = test_dir + "/out/" + in_file[:-3] + ".out"
        temp_file = (test_dir + "/temp/" + in_file[:-3]
                     + ".out" if config.keep_temp else generate_tempfile())

        if not is_valid_path(out_file):
            print(f"File \"{in_file}\"".ljust(20) + "MISSING_OUT")

        subprocess.run(
            config.run_exec_cmd.format(exec=remove_blank_whitespaces(config.exec_path),
                                       in_file=remove_blank_whitespaces(in_file),
                                       temp_file=remove_blank_whitespaces(temp_file)))

        is_correct = self.is_correct(out_file, temp_file)

        if is_correct:
            verbose_print(f"File \"{in_file}\"".ljust(20) + "OK")
        else:
            print(f"File \"{in_file}\"".ljust(20) + "WRONG")

        return is_correct

    def is_correct(self, out_file: str, temp_file: str) -> bool:
        if config.is_using_custom_checker():
            return subprocess.run(
                config.run_custom_checker_cmd.format(
                    checker=remove_blank_whitespaces(cast(str, config.custom_checker_path)),
                    temp_file=remove_blank_whitespaces(temp_file))).returncode == 0
        else:
            return filecmp.cmp(out_file, temp_file)

    def print_results(self) -> None:
        for result in self.results:
            print(
                f"Test dir \"{result[0]}\"".ljust(20) +
                f"TOTAL: {result[1]:>4}  CORRECT: {result[2]:>4}  WRONG: {result[1] - result[2]:>4}"
            )



def main() -> None:
    config.parse_argv()

    tester = Tester()
    tester.test_all().print_results()



if __name__ == "__main__":
    main()
