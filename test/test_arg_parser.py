import sys

sys.path.append("../src")
# Uncomment if when debugging python is having trouble importing arg_parser
# sys.path.append("./src")

import unittest
import arg_parser
from arg_parser import ArgParser



class ArgParserTest(unittest.TestCase):
    def test_constructor_fails_with_no_args(self) -> None:
        try:
            parser = ArgParser()
            self.fail()
        except TypeError:
            pass

    def test_constructor_fails_with_only_named_actor(self) -> None:
        try:
            parser = ArgParser(arg_actors=[])
            self.fail()
        except TypeError:
            pass

    def test_constructor_fails_with_only_default_actor(self) -> None:
        try:
            parser = ArgParser(default_arg_actor=lambda _1, _2: None)
            self.fail()
        except TypeError:
            pass

    def test_constructor_allows_both_arguments(self) -> None:
        try:
            parser = ArgParser(arg_actors=[], default_arg_actor=lambda _1, _2: None)
        except TypeError:
            self.fail()

    def test_named_actors_added_correctly(self) -> None:
        a: int = 0
        b: int = 0

        def inc_a(_1, _2) -> None:
            nonlocal a
            a += 1

        def inc_b(_1, _2) -> None:
            nonlocal b
            b += 1

        def def_actor(_1, _2) -> None:
            pass

        parser = ArgParser(arg_actors=[("-a", inc_a), (["-b", "--inc-b"], inc_b)],
                           default_arg_actor=def_actor)

        self.assertEqual(parser.arg_actors, {"-a": inc_a, "-b": inc_b, "--inc-b": inc_b})
        self.assertEqual(parser.default_arg_actor, def_actor)

    def test_default_actor_added_correctly(self) -> None:
        a: int = 0

        def def_actor(_1, _2) -> None:
            nonlocal a
            a += 2

        parser = ArgParser(arg_actors=[], default_arg_actor=def_actor)

        self.assertEqual(parser.default_arg_actor, def_actor)
        self.assertDictEqual(parser.arg_actors, {})

    def test_isolated_named_actors_execute_correctly(self) -> None:
        a: int = 0
        b: int = 0

        def inc_a(_1, _2) -> None:
            nonlocal a
            a += 1

        def inc_b(arg: str, _2) -> None:
            nonlocal b
            b += 1 if arg == "-b" else 2

        parser = ArgParser(arg_actors=[(["-a", "--inc-a"], inc_a), (["-b", "--inc-b"], inc_b)],
                           default_arg_actor=lambda _1, _2: None)
        parser.parse("-a -b -blah --inc-a --inc-b inc-b b a inc-a".split(" "))

        self.assertEqual((a, b), (2, 3))

    def test_isolated_default_actor_executes_correctly(self) -> None:
        a: int = 0
        b: int = 0
        other: int = 0

        def def_actor(arg: str, _2) -> None:
            nonlocal a, b, other

            if arg == "a":
                a += 1
            elif arg == "b":
                b += 1
            else:
                other += 1

        parser = ArgParser(arg_actors=[], default_arg_actor=def_actor)
        parser.parse("a b -a -b --a --inc-a --inc-b inc_a inc_b a a b".split(" "))

        self.assertEqual((a, b, other), (3, 2, 7))

    def test_actors_get_parameters_correctly(self) -> None:
        a: int = 0
        b: int = 0
        other: int = 0

        def inc_a(_1, parser: ArgParser) -> None:
            nonlocal a
            try:
                a += int(parser.get_next_arg())
            except arg_parser.NoNextArgument:
                a = 1000

        def inc_b(_1, parser: ArgParser) -> None:
            nonlocal b
            b += int(parser.get_next_arg_or(100))

        def def_actor(_1, parser: ArgParser) -> None:
            nonlocal other
            other += int(parser.get_next_arg_or(10000))

        parser = ArgParser(arg_actors=[(["-a", "--inc-a"], inc_a), ("-b", inc_b)],
                           default_arg_actor=def_actor)
        parser.parse("-a 1 --a 2 --inc-b 1 -b 1 -a 3 -b 2 --inc-a".split(" "))

        self.assertEqual((a, b, other), (1000, 3, 3))



if __name__ == "__main__":
    unittest.main()
