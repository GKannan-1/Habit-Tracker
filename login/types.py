from typing import Protocol, cast


class HasID(Protocol):
    id: int
