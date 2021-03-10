from typing import Optional, List
import psycopg2
import psycopg2.extensions
import os
import sql
from models import Hero


def get_conn() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_DATABASE'],
        port=os.environ['DB_PORT'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )


conn = get_conn()


def set_hero(hero: Hero) -> None:
    cur = conn.cursor()

    query = sql.INSERT_HERO
    cur.execute(query, (hero.id, hero.name, hero.description, hero.picture))
    conn.commit()

    cur.close()
