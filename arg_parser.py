# Prosty kod pozwalający na łatwe parowanie argumentów.
# Przemysław Tracz, Warszawa 11 lis 2021

from __future__ import annotations


class ArgParser:
    arg_values: list[str]
    arg_actions: dict[str, arg_action]
    default_arg_action: arg_action
    arg_index: int  # Used for parse() and parse_next_argument()

    def __init__(self, arg_values: list[str] = [], arg_actions: dict[str, arg_action] = {}, default_arg_action: arg_action = ()):
        self.arg_values = arg_values
        self.arg_actions = arg_actions
        self.default_arg_action = default_arg_action
        self.arg_index = 0

    def set_arg_action(self, key: str, action: arg_action) -> None:
        self.arg_actions[key] = action

    def set_default_arg_action(self, action: arg_action) -> None:
        self.default_arg_action = action

    def parse_next_argument(self) -> str:
        self.arg_index += 1
        return self.arg_values[self.arg_index]

    def parse(self) -> None:
        while self.arg_index < len(self.arg_values):
            if self.arg_values[self.arg_index] in self.arg_actions:
                self.arg_actions[self.arg_values[self.arg_index]].parse(
                    self.arg_values[self.arg_index], self)
            else:
                self.default_arg_action.parse(
                    self.arg_values[self.arg_index], self)

            self.arg_index += 1


class arg_action:
    # Override this method to have custom parsing actions
    def parse(self, argument: str, parser: ArgParser) -> None:
        pass

    # Do not override this function
    def __missing__(self, key) -> arg_action:
        return arg_action()
