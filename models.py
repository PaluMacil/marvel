from dataclasses import dataclass


@dataclass
class Hero:
    id: int
    name: str
    description: str
    picture: bytes
