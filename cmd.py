from typing import List

import db
import marvel
from models import Hero, Comic


def find_hero(name: str, verbose: bool = False) -> Hero:
    hero = db.get_hero(name=name)
    from_db = bool(hero)
    if not hero:
        hero = marvel.fetch_hero(name)
    if not hero:
        raise Exception(f'hero {name} not found')
    if not from_db:
        db.set_hero(hero)

    return hero


def find_associated_heroes(name: str, verbose: bool = False) -> List[Hero]:
    heroes: List[Hero] = []

    main_hero = find_hero(name, verbose)
    # get comic_ids for comics that don't require a remote fetch
    scanned_comic_ids = (comic.id for comic in db.get_comics())
    for comic_id in main_hero.appearances:
        # check whether we already have all the data on this comic in the db
        if any(comic_id == scanned_id for scanned_id in scanned_comic_ids):
            heroes.extend(db.get_heroes(comic_id))
        else:
            heroes.extend(marvel.fetch_heroes(comic_id))
            # once a comic is fully fetched, create a record for it so
            # that this comic can be queried from the db in the future
            # instead of fetching from the API again
            db.set_comic(Comic(comic_id))
    # deduplicate heroes (most heroes appear in multiple comics)
    heroes = list(set(heroes))
    # save any heroes not yet in the database
    for hero in heroes:
        db.set_hero(hero, True)

    print(f'found {name} and {len(heroes)} associates:')
    print(', '.join([hero.name for hero in heroes]))

    return heroes
