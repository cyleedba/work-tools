import boto3

# initial S3 setting
s3_client = boto3.client('s3', region_name='ap-east-1')

# setting S3 bucket name
bucket_name = 'apple-redis-rbd'
file_name = 'film-backup-0001.rdb'

# your local file location 
local_file_name = '/home/pro_dba/film-backup-0001.rdb'

# execute s3 download 
s3_client.download_file(bucket_name, file_name, local_file_name)

print(f"{file_name} has been downloaded to {local_file_name}")
