from dataclasses import dataclass
from typing import List


@dataclass
class Hero:
    id: int
    name: str
    description: str
    picture: bytes
    appearances: List[int]


@dataclass
class ComicHero:
    hero_id: int
    comic_id: int


@dataclass
class Comic:
    id: int
