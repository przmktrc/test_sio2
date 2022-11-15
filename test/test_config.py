import sys

sys.path.append("./src")
sys.path.append(".")

import unittest
from config import remove_blank_whitespaces, is_valid_path, config, InvalidConfig
from path_to_here import path_to_here



class TestHelperFunctions(unittest.TestCase):
    def test_remove_blank_whitespace_single(self) -> None:
        self.assertEqual(remove_blank_whitespaces("blah blah"), "blah\ blah")
        self.assertEqual(remove_blank_whitespaces("remove blank whitespaces from this string"),
                         "remove\ blank\ whitespaces\ from\ this\ string")

    def test_remove_blank_whitespace_list(self) -> None:
        self.assertEqual(remove_blank_whitespaces(["remove blank", "white spaces", "from_here"]),
                         ["remove\ blank", "white\ spaces", "from_here"])
        self.assertNotEqual(remove_blank_whitespaces(["remove blank", "white_spaces"]),
                            ["remove\ blank", "white\ spaces"])

    def test_is_valid_path(self) -> None:
        self.assertTrue(is_valid_path("/home"))
        self.assertFalse(is_valid_path("/nonexistant"))
        self.assertTrue(is_valid_path(path_to_here + "/test"))
        self.assertTrue(is_valid_path(path_to_here + "/test/sample project repeater"))



class TestConfigWithSetValues(unittest.TestCase):
    def setUp(self) -> None:
        config.parse_argv([
            "--verbose", "--notemp", "-e", "test/sample project repeater/repeater.sh",
            "test/sample project repeater/test_same_out", "--checker",
            "test/sample project repeater/checker.sh"
        ])

    def test_parsed_verbose(self) -> None:
        self.assertTrue(config.verbose)

    def test_parsed_notemp(self) -> None:
        self.assertFalse(config.keep_temp)

    def test_parsed_existing_exec(self) -> None:
        try:
            self.assertEqual(config.exec_path,
                             path_to_here + "/test/sample project repeater/repeater.sh")
        except InvalidConfig:
            self.fail()

    def test_parsed_nonexistant_exec(self) -> None:
        self.assertRaisesRegex(InvalidConfig, "Invalid executable path", config.parse_argv,
                               ["--exec", "some/nonexistant-path"])

    def test_parsed_existing_checker(self) -> None:
        try:
            self.assertEqual(config.custom_checker_path,
                             path_to_here + "/test/sample project repeater/checker.sh")
        except InvalidConfig:
            self.fail()

    def test_parsed_nonexistant_checker(self) -> None:
        self.assertRaisesRegex(InvalidConfig, "Invalid checker path", config.parse_argv,
                               ["-v", "--checker", "test/nonexistant_path"])

    def test_parsed_existing_test_dirs(self) -> None:
        self.assertEqual(config.test_dirs,
                         [path_to_here + "/test/sample project repeater/test_same_out"])

    def test_parsed_nonexistant_test_dirs(self) -> None:
        self.assertRaisesRegex(InvalidConfig, "Invalid test dir", config.parse_argv,
                               ["test/sample project repeater/test_same_out", "nonexistant_path"])
        self.assertRaisesRegex(InvalidConfig, "nonexistant_path", config.parse_argv,
                               ["test/sample project repeater/test_same_out", "nonexistant_path"])

    def test_reset(self) -> None:
        self.assertTrue(config.verbose)
        self.assertFalse(config.keep_temp)
        config.reset()
        self.assertFalse(config.verbose)
        self.assertTrue(config.keep_temp)



if __name__ == "__main__":
    unittest.main()
