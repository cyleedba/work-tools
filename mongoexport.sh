# mongoexport command
# change dbname . host . collection . fields .port 
mongoexport -u gcp_replica -p 123qwe --db apple_record --authenticationDatabase admin --host xxx.xxx.xxx.xxx --port xxxx --authenticationMechanism SCRAM-SHA-256 --collection=core_sns_mdclickcountsummary --type=csv --fields=id,sns_id,sns_type,app_code,click_count,created_date --out=/home/pro_dba/export.csv
