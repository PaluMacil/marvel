create table if not exists hero (
	id integer primary key,
	name text not null,
	description text not null,
	picture BYTEA NOT NULL
);

create table if not exists comic_hero (
	hero_id integer,
	comic_id integer,
    primary key(hero_id, comic_id)
);

create table if not exists comic (
    id integer primary key
);