from typing import List
import marvel
import db
from models import Hero


def find_associated_heroes(name: str) -> List[Hero]:
    heroes: List[Hero] = []

    main_hero = marvel.fetch_hero(name=name)
    associated_ids = marvel.fetch_associated_ids(main_hero.id)
    for id in associated_ids:
        hero = marvel.fetch_hero(id)
        heroes.append(hero)
        db.set_hero(hero)

    print(f'found {len(heroes)} characters:')
    print(', '.join([hero.name for hero in heroes]))

    return heroes
