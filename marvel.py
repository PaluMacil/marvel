import time
import os
from typing import List, Optional

import requests
from hashlib import md5
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


def fetch_thumbnail(partial_url) -> bytes:
    url = f"{partial_url}/standard_medium.jpg"
    resp = requests.get(url, auth_params())

    if not resp.ok:
        raise Exception(f'fetching thumbnail at {url}: {resp.text}')
    resp.raw.decode_content = True

    return resp.content


def fetch_associated_ids(hero_id: int) -> List[int]:
    url = f'https://gateway.marvel.com/v1/public/characters/{hero_id}/comics'
    params = auth_params()
    params.update({
        'limit': PAGE_LIMIT,
        'orderBy': 'title'
    })
    resp = requests.get(url, params)
    if not resp.ok:
        raise Exception(f'fetching comics for hero id {hero_id}: {resp.text}')

    data_object = resp.json()['data']
    characters = [comic_object['characters']['items'] for comic_object in data_object['results']]
    # flatten list of character lists to list of characters
    characters = sum(characters, [])
    character_uris = [character['resourceURI'] for character in characters]
    character_ids = [int(uri.split('/')[-1]) for uri in character_uris]
    # get distinct list
    character_ids = list(set(character_ids))

    return character_ids


def parse_hero(data) -> Hero:
    id = data['id']
    name = data['name']
    description = data['description']
    picture_url = data['thumbnail']['path']
    picture = fetch_thumbnail(picture_url)

    return Hero(id=id,
                name=name,
                description=description,
                picture=picture)


def fetch_hero(id: Optional[int] = None, name: Optional[str] = None) -> Hero:
    if id and name:
        raise Exception('cannot use both id and name in same search')
    url = 'https://gateway.marvel.com/v1/public/characters'
    if id:
        url = f'{url}/{id}'
    params = auth_params()
    if name:
        params.update({
            'name': name,
        })
    resp = requests.get(url, params)
    if not resp.ok:
        raise Exception(f'fetching : ' + resp.text)
    data = resp.json()['data']['results'][0]
    hero = parse_hero(data)

    return hero
