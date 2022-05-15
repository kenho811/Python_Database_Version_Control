insert into dvc.database_revision_history
  (
	executed_sql_file_folder,
	executed_sql_file_name,
	executed_sql_file_content_hash,
	executed_sql_file_content,
	operation
  )
  values
  (%s,%s,%s,%s, %s);
