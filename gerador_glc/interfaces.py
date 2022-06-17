from typing import TypedDict


class Grammar(TypedDict):
    initial: str
    productions: dict[str, list[str]]
    terminals: list[str]
    variables: list[str]
