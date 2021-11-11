import arg_parser
import os


class Config:
    count: int
    is_quiet: bool
    do_keep_temp: bool
    parent_dir: str
    program_path: str
    test_dir: str

    def __init__(self):
        self.count = 1000000000
        self.is_quiet = False
        self.do_keep_temp = True
        self.parent_dir = os.getcwd()
        self.program_path = ""
        self.test_dir = self.parent_dir + "/test"

    def print_config(self):
        print("count {}\nis_quiet {}\nkeep_temp {}\nparent_dir {}\nprogram_path {}\ntest_dir {}".format(
            self.count, self.is_quiet, self.do_keep_temp, self.parent_dir, self.program_path, self.test_dir))


config = Config()


class set_count(arg_parser.arg_action):
    def parse(self, key: str, parser: arg_parser.ArgParser):
        config.count = int(parser.parse_next_argument())


class set_testdir(arg_parser.arg_action):
    def parse(self, key: str, parser: arg_parser.ArgParser):
        config.test_dir = config.parent_dir + "/" + parser.parse_next_argument()


class set_keep_quiet(arg_parser.arg_action):
    def parse(self, key: str, parser: arg_parser.ArgParser):
        config.is_quiet = True


class set_notemp(arg_parser.arg_action):
    def parse(self, key: str, parser: arg_parser.ArgParser):
        config.do_keep_temp = False


class set_program(arg_parser.arg_action):
    def parse(self, key: str, parser: arg_parser.ArgParser):
        if config.program_path != "":
            print("Warning: Program path specified more than once. Ignoring \"{}\" and proceeding with \"{}\".".format(
                key, config.program_path))
            return

        config.program_path = config.parent_dir + "/" + key


class print_help(arg_parser.arg_action):
    def parse(self, key: str, parser: arg_parser.ArgParser):
        print(
            "Usage:\n    test_sio2 \033[4mprogram_path\033[0m [-c | --count \033[4mcount\033[0m] [--testdir \033[4mtest_dir\033[0m] [--quiet] [--notemp] [-h | --help]")
        exit(0)
