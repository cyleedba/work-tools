import boto3
import time

# Initialize the Redshift Data client
client = boto3.client('redshift-data', region_name='ap-northeast-1')

DATABASE_NAME = 'dev'
CLUSTER_ID = 'dev-test'
SECRET_ARN = 'your-secret-arn'
DB_USER= 'admin'

# SQL 查詢以獲取所有表格名稱
LIST_TABLES_SQL = """  CREATE TABLE core_analysis_mddashboardglobal (
    id integer NOT NULL,
    date_range integer NOT NULL,
    active_user integer NOT NULL,
    new_user integer NOT NULL,
    new_pay_user integer NOT NULL,
    withdraw_user integer NOT NULL,
    live_pay_user integer NOT NULL,
    valid_bet_user integer default 0,
    game_bet_return_user integer default 0,
    game_bet_win integer default 0,
    online_user integer NOT NULL,
    created_date date not null,
    created_time timestamp without time zone not null,
    PRIMARY KEY (id)
) DISTSTYLE AUTO
SORTKEY (id);
"""

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

# 檢查查詢是否成功完成
if status == 'FINISHED':
    print("Table created successfully.")
elif status in ['FAILED', 'ABORTED']:
    print("Table creation failed.")
