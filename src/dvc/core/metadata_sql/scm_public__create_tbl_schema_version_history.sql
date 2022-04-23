create schema if not exists public;
create table if not exists public.schema_version_history(
	id serial primary key,
	sql_file_name_applied varchar(255) not null,
	sql_file_content_hash varchar(255) not null,
	operation varchar(20) not null,
    created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc')
);
