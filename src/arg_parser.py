from typing import Callable, Iterator, Any



class NoNextArgument(RuntimeError):
    pass



class ArgParser():
    ArgActor = Callable[[str, "ArgParser"], None]
    NamedActor = tuple[list[str] | str, ArgActor]

    arg_actors: dict[str, ArgActor] = {}
    default_arg_actor: ArgActor

    arg_iterator: Iterator[str]

    def __init__(self, arg_actors: list[NamedActor], default_arg_actor: ArgActor):
        self.default_arg_actor = default_arg_actor
        self.arg_actors = {}
        self.add_arg_actors(arg_actors)

    def add_arg_actors(self, named_actors: list[NamedActor]) -> None:
        for named_actor in named_actors:
            if isinstance(named_actor[0], list):
                for arg_name in named_actor[0]:
                    self.arg_actors[arg_name] = named_actor[1]
            else:
                self.arg_actors[named_actor[0]] = named_actor[1]

    def parse(self, arg_values: list[str]) -> None:
        self.arg_iterator = iter(arg_values)

        while (arg_value := next(self.arg_iterator, None)) is not None:
            self.parse_arg(arg_value)

    def parse_arg(self, arg: str) -> None:
        if arg in self.arg_actors:
            self.arg_actors[arg](arg, self)
        else:
            self.default_arg_actor(arg, self)

    def get_next_arg(self) -> str:
        try:
            return next(self.arg_iterator)
        except StopIteration:
            raise NoNextArgument("There is no next argument")

    def get_next_arg_or(self, default_value: Any) -> str | Any:
        return next(self.arg_iterator, default_value)
