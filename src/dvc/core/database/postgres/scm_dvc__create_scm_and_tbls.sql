-- create dvc schema
create schema if not exists dvc;
-- create database_revision_history table
create table if not exists dvc.database_revision_history(
	revision_id serial primary key,
	executed_sql_file_folder varchar(255) not null,
	-- SQL File Name must follow a certain pattern
	executed_sql_file_name varchar(255) not null check (executed_sql_file_name ~ 'RV[0-9]*__.*\.(upgrade|downgrade)\.sql'),
	executed_sql_file_content_hash varchar(255) not null,
	executed_sql_file_content text not null,
	-- Operation must be either Upgrade or Downgrade
	operation varchar(20) not null check (operation ~ '(Upgrade|Downgrade)'),
	-- Revision applied must be the first part of the file name
	revision_applied varchar(20) GENERATED ALWAYS AS (split_part(executed_sql_file_name, '__', 1)) STORED,
    created_at TIMESTAMP not null default (now() at time zone 'utc')
);
-- create database_version_history table
create table if not exists dvc.database_version_history(
	version_id serial primary key,
	current_version_number varchar(255),
	revision_id_applied integer not null,
    created_at TIMESTAMP not null default (now() at time zone 'utc'),
    CONSTRAINT fk_database_revision_history FOREIGN KEY(revision_id_applied) REFERENCES dvc.database_revision_history(revision_id) ON DELETE RESTRICT
);
-- create trigger function for auto-insertion
create or replace
function dvc.fn_database_version_history_insert_trigger()
returns trigger as
$$
begin
    insert
	into
	dvc.database_version_history (
	"current_version_number",
	"revision_id_applied" ,
	"created_at"
	)
values(
CASE NEW."operation" WHEN 'Upgrade' then 'V'||SUBSTRING(NEW.REVISION_APPLIED,3):: integer else 'V'||SUBSTRING(NEW.REVISION_APPLIED,3):: integer -1 end,
NEW."revision_id",
now() at time zone 'utc');
return new;
end;
$$
language 'plpgsql';
-- Postgresql <= 13 cannot create or replace trigger
drop trigger if exists "database_version_history_insert_trigger" ON dvc."database_revision_history";
CREATE trigger "database_version_history_insert_trigger"
AFTER INSERT
ON dvc."database_revision_history"
FOR EACH ROW
EXECUTE PROCEDURE dvc.fn_database_version_history_insert_trigger();