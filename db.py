from typing import Optional, List
import psycopg2
import psycopg2.extensions
from psycopg2.extras import DictCursor, execute_values
import os
import sql
from models import Hero, Comic


def get_conn() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_DATABASE'],
        port=os.environ['DB_PORT'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )


conn = get_conn()


def get_hero_ids(comic_id: int) -> List[int]:
    cur = conn.cursor()
    cur.execute(sql.SELECT_HERO_IDS_BY_COMIC, (comic_id,))
    return [item[0] for item in cur.fetchall()]


def get_hero(id: Optional[int] = None, name: Optional[str] = None) -> Optional[Hero]:
    cur = conn.cursor(cursor_factory=DictCursor)
    hero_query = sql.SELECT_HERO_BY_ID if id else sql.SELECT_HERO_BY_NAME
    identifier = id or name
    cur.execute(hero_query, (identifier,))
    hero_obj = cur.fetchone()
    if not hero_obj:
        return None
    hero = Hero(id=hero_obj['id'],
                name=hero_obj['name'],
                description=hero_obj['description'],
                picture=hero_obj['picture'],
                appearances=[])

    # get comic ids associate with this hero
    cur.execute(sql.SELECT_COMIC_IDS, (hero.id,))
    comic_ids = [item['id'] for item in cur.fetchall()]
    hero.appearances = comic_ids

    cur.close()

    return hero


def get_heroes(comic_id: int) -> List[Hero]:
    return [get_hero(id) for id in get_hero_ids(comic_id)]


def set_hero(hero: Hero, check_first: bool = False) -> None:
    # if requested, check if hero already exists and abort insertion if it does
    if check_first and get_hero(hero.id):
        return

    cur = conn.cursor()

    query = sql.INSERT_HERO
    cur.execute(query, (hero.id, hero.name, hero.description, hero.picture))
    conn.commit()

    # insert appearances
    rows = map(lambda comic_id: (hero.id, comic_id), hero.appearances)
    execute_values(cur, sql.INSERT_COMIC_HERO, rows)
    conn.commit()

    cur.close()


def set_comic(comic: Comic) -> None:
    cur = conn.cursor()
    query = sql.INSERT_COMIC
    cur.execute(query, (comic.id,))
    conn.commit()


def get_comics() -> List[Comic]:
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute(sql.SELECT_COMICS)
    return [Comic(rec['id']) for rec in cur.fetchall()]
