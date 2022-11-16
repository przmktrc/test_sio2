def print_help() -> None:
    print(
        "test_sio2\n"
        "SYNTAX\n"
        "    test_sio2 [-h | --help] [-v | --verbose] [--notemp] [--checker <checker>] -e <executable> <test_dir>...\n\n"
        "OPTIONS\n"
        "    -e | --exec <exec>\n"
        "        Provide an executable to test\n"
        "    -v | --verbose\n"
        "        Print successful checks as well as failed ones\n"
        "    --notemp\n"
        "        Don't store outputs in <test_dir>/temp/\n"
        "    --checker <checker>\n"
        "        Provide a custom checker.\n"
        "        The checker should read data from stdin and exit with 0 for success.\n"
        "    -h | --help\n"
        "        Print this here help menu\n")
