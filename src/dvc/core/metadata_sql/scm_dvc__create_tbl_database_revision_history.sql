create schema if not exists dvc;
create table if not exists dvc.database_revision_history(
	revision_id serial primary key,
	executed_sql_file_folder varchar(255) not null,
	-- SQL File Name must follow a certain pattern
	executed_sql_file_name varchar(255) not null check (executed_sql_file_name ~ 'RV[0-9]*__.*\.(upgrade|downgrade)\.sql'),
	executed_sql_file_content_hash varchar(255) not null,
	-- Operation must be either Upgrade or Downgrade
	operation varchar(20) not null check (operation ~ '(Upgrade|Downgrade)'),
    created_at TIMESTAMP not null default (now() at time zone 'utc')
);
