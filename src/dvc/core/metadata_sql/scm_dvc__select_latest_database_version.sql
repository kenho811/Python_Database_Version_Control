with max_version_id (max_version_id) as(
select
		max(version_id)
from
		dvc.database_version_history
)
select
	current_version_number ,
	'RV'||((substring(current_version_number, 2)::integer) + 1)::text as next_upgrade_revision_version,
	'RV'||((substring(current_version_number, 2)::integer))::text as next_downgrade_revision_version,
	created_at
from
	dvc.database_version_history dvh
where
	version_id = (
	select
		max_version_id
	from
		max_version_id)