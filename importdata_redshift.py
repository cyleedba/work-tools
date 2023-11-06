import boto3
import time

# Initialize the Redshift Data client
client = boto3.client('redshift-data', region_name='ap-northeast-1')

DATABASE_NAME = 'dev'
CLUSTER_ID = 'dev-test'
SECRET_ARN = 'your-secret-arn'
DB_USER= 'admin'

# COPY 命令
COPY_SQL = """
    COPY dev.public.core_sns_mdclickcountsummary (id, sns_id, sns_type, app_code, click_count, created_date)
    FROM 's3://mysqldb-log/export.csv'
    IAM_ROLE 'aws_iam_role=your-iam-role'
    FORMAT AS CSV DELIMITER ',' IGNOREHEADER 1
    DATEFORMAT 'auto' TIMEFORMAT 'auto'
    REGION AS 'ap-northeast-1';
"""
# 執行 COPY 命令
response = client.execute_statement(
    ClusterIdentifier=CLUSTER_ID,
    Database=DATABASE_NAME,
    SecretArn=SECRET_ARN,
    Sql=COPY_SQL
)

query_id = response['Id']

# 等待查詢完成
while True:
    status_response = client.describe_statement(Id=query_id)
    status = status_response['Status']
    if status in ['FINISHED', 'FAILED', 'ABORTED']:
        break
    time.sleep(5)  # 每5秒檢查一次查詢的狀態

# 檢查查詢結果
if status == 'FINISHED':
    print("COPY command completed successfully.")
elif status in ['FAILED', 'ABORTED']:
    print(f"COPY command failed with error: {status_response['Error']}")
