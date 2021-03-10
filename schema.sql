create table if not exists hero (
	id integer primary key,
	name text not null,
	description text not null,
	picture BYTEA NOT NULL
);
