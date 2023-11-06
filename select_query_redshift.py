import boto3
import time

# Initialize the Redshift Data client
client = boto3.client('redshift-data', region_name='ap-northeast-1')

DATABASE_NAME = 'dev'
CLUSTER_ID = 'dev-test'
SECRET_ARN = 'your-secret-arn'
DB_USER= 'admin'

# SQL 查詢以獲取所有表格名稱
LIST_TABLES_SQL = """ SELECT * FROM pg_catalog.stl_load_errors; """

# 執行 SQL 查詢
response = client.execute_statement(
    ClusterIdentifier=CLUSTER_ID,
    Database=DATABASE_NAME,
    SecretArn=SECRET_ARN,
    Sql=LIST_TABLES_SQL
)

query_id = response['Id']
# 等待查詢完成
while True:
    status_response = client.describe_statement(Id=query_id)
    status = status_response['Status']
    if status in ['FINISHED', 'FAILED', 'ABORTED']:
        break
    time.sleep(1)  # 每秒檢查一次查詢的狀態

# 抓取查詢結果
results = client.get_statement_result(Id=query_id)
for record in results['Records']:
    print(record)
