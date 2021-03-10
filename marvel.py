import time
import os
from typing import List

import requests
from hashlib import md5
import db
from models import Hero

# API's max page limit for a resource type
PAGE_LIMIT = 100


def auth_params():
    timestamp = str(int(time.time()))
    public_key = os.environ['MARVEL_PUBLIC_KEY']
    private_key = os.environ['MARVEL_PRIVATE_KEY']
    key_hash = md5((timestamp + private_key + public_key).encode('utf-8')).hexdigest()
    return {
        'ts': timestamp,
        'apikey': public_key,
        'hash': key_hash
    }


def fetch_thumbnail(partial_url):
    url = f"{partial_url}/standard_medium.jpg"
    resp = requests.get(url, auth_params())

    if not resp.ok:
        raise Exception(f'fetching thumbnail at {url}: {resp.text}')
    resp.raw.decode_content = True

    return resp.content


def fetch_appearances(hero_id: int, **kwargs) -> List[int]:
    url = f'https://gateway.marvel.com/v1/public/characters/{hero_id}/comics'
    offset = kwargs.get('offset', 0)
    comic_ids: List[int] = kwargs.get('comic_ids', [])
    params = auth_params()
    params.update({
        'limit': PAGE_LIMIT,
        'offset': str(offset),
        'orderBy': 'title'
    })
    resp = requests.get(url, params)
    if not resp.ok:
        raise Exception(f'fetching comics for hero id {hero_id}: {resp.text}')

    data_object = resp.json()['data']
    new_ids: List[int] = [comic_object['id'] for comic_object in data_object['results']]
    comic_ids.extend(new_ids)
    retrieved_count = len(comic_ids)
    total_comics = data_object['total']

    if retrieved_count < total_comics:
        return fetch_appearances(hero_id,
                                 offset=offset + PAGE_LIMIT,
                                 comic_ids=comic_ids)

    return comic_ids


def parse_hero(data) -> Hero:
    id = data['id']
    name = data['name']
    description = data['description']
    picture_url = data['thumbnail']['path']
    picture = fetch_thumbnail(picture_url)
    comic_uris = (item['resourceURI'] for item in data['comics']['items'])
    comic_ids = [int(uri.split('/')[-1]) for uri in comic_uris]
    total_comics = data['comics']['available']
    if len(comic_ids) < total_comics:
        # don't reuse the first 20 from here because we can't control the orderby
        comic_ids = fetch_appearances(id)
    return Hero(id=id,
                name=name,
                description=description,
                picture=picture,
                appearances=comic_ids)


def fetch_hero(name: str) -> Hero:
    hero = db.get_hero(name=name)
    if hero:
        return hero

    url = 'https://gateway.marvel.com/v1/public/characters'
    params = auth_params()
    params.update({
        'nameStartsWith': name,
        'limit': 2
    })
    resp = requests.get(url, params)
    if not resp.ok:
        raise Exception(f'fetching : ' + resp.text)
    data = resp.json()['data']['results'][0]
    hero = parse_hero(data)

    return hero


def fetch_heroes(comic_id: int, **kwargs) -> List[Hero]:
    url = f'https://gateway.marvel.com/v1/public/comics/{comic_id}/characters'
    offset = kwargs.get('offset', 0)
    all_heroes: List[Hero] = kwargs.get('heroes', [])

    params = auth_params()
    params.update({
        'limit': PAGE_LIMIT,
        'offset': str(offset),
        'orderBy': 'name'
    })
    resp = requests.get(url, params)
    if not resp.ok:
        raise Exception('fetching characters: ' + resp.text)

    data_object = resp.json()['data']
    new_heroes = [parse_hero(hero_data) for hero_data in data_object['results']]
    all_heroes.extend(new_heroes)
    retrieved_count = len(all_heroes)
    total_heroes = data_object['total']

    if retrieved_count < total_heroes:
        return fetch_heroes(comic_id,
                            offset=offset + PAGE_LIMIT,
                            heroes=all_heroes)

    return all_heroes
