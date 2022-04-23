insert into public.schema_version_history
  (
	sql_file_name_applied,
	sql_file_content_hash,
	operation
  )
  values
  (%s,%s,%s);
