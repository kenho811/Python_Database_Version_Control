with max_id (max_id) as(
select
		max(id)
from
		dvc.dvc_revision_history
)
select
	id,
	sql_file_name_applied ,
	sql_file_content_hash ,
	operation ,
	created_at
from
	dvc.database_revision_history srh
where
	id = (
	select
		max_id
	from
		max_id)