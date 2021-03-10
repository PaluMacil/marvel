# Select statements

SELECT_HERO_BY_NAME = '''
select id, name, description, picture 
from hero 
where name=%s
'''

SELECT_HERO_BY_ID = '''
select id, name, description, picture 
from hero 
where id=%d
'''

SELECT_COMIC_IDS = '''
select ch.comic_id as id
from comic_hero ch
where ch.hero_id = %s
'''

SELECT_HERO_IDS_BY_COMIC = '''
select h.id as id 
from hero h
join comic_hero ch
    on h.id = ch.hero_id
where ch.comic_id = %s
'''

SELECT_COMICS = '''
select id
from comic
'''

# Insert statements

INSERT_HERO = '''
insert into hero 
    (id, name, description, picture) 
values
    (%s, %s, %s, %s)
'''

INSERT_COMIC_HERO = '''
insert into comic_hero
    (hero_id, comic_id)
values %s
'''

INSERT_COMIC = '''
insert into comic
    (id)
values
    (%s)
'''