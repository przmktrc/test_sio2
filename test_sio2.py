import sys
import config
import arg_parser
import re
import os
import filecmp


def remove_blank_whitespace(path: str) -> str:
    return re.sub(r" ", "\ ", path)


def run_signle_test(file: str):
    file_in = config.config.test_dir + "/in/" + file
    file_out = config.config.test_dir + \
        "/out/" + file[:len(file) - 3] + ".out"
    file_temp = config.config.test_dir + \
        "/temp/" + \
        file[:len(file) - 3] + \
        ".out" if config.config.do_keep_temp else config.config.test_dir + "/__temp.out"

    if os.path.isfile(file_in) and os.path.isfile(file_out):
        os.system(remove_blank_whitespace(config.config.program_path) + " < " + remove_blank_whitespace(file_in) +
                  " > " + remove_blank_whitespace(file_temp))

        result = filecmp.cmp(file_temp, file_out)

        if config.config.is_quiet:
            if not result:
                print(file.ljust(20) + "WRONG")
        else:
            print(file.ljust(20) +
                  ("OK" if result else "WRONG"))
    else:
        if not config.config.is_quiet:
            print(file.ljust(20) + "FILE MISSING")


def main():
    parser = arg_parser.ArgParser(sys.argv[1:], {
                                  "-c": config.set_count(), "--count": config.set_count(), "--quiet": config.set_keep_quiet(), "--notemp": config.set_notemp(), "--testdir": config.set_testdir(), "-h": config.print_help(), "--help": config.print_help()}, config.set_program())
    parser.parse()

    # If no arguments were provided, the user is probably new to this script
    if len(sys.argv) == 1:
        print("Warning: No arguments provided. Run with --help for more information.")

    # If the program does not exists, print a message and exit
    if not os.path.isfile(config.config.program_path):
        print("Error: Program \"{}\" not found. Exiting.".format(
            config.config.program_path))
        exit(1)

    i = 0
    for file in os.listdir(config.config.test_dir + "/in"):
        if i > config.config.count:
            break

        run_signle_test(file)

        i += 1

    # If running with --notemp flag, delete the temp file
    if not config.config.do_keep_temp:
        os.remove(config.config.test_dir + "/__temp.out")


if __name__ == "__main__":
    main()
