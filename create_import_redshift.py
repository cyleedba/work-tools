import boto3
import time

# 初始化 redshift-data 客户端
client = boto3.client('redshift-data')

DATABASE_NAME = 'dev'
CLUSTER_ID = 'dev-test'
SECRET_ARN = 'arn:aws:secretsmanager:ap-northeast-1:717906228860:secret:RedshiftCredentials-HakB2o'
# AWS Secrets Manager 的 ARN，其中包含 Redshift 凭证
DB_USER= 'admin'

# SQL 创建表格的语句
CREATE_TABLE_SQL = """
    CREATE TABLE public.core_analysis_mdglobaluserconsumereport (
        id integer NOT NULL,
        buy_vip integer NOT NULL,
        live_tip integer default 0,
        live_ticket integer default 0,
        tip_post integer NOT NULL,
        game_expense_and_income_sum integer not null,
        buy_video integer default 0,
        created_date date not null,
        created_time timestamp without time zone not null,
        PRIMARY KEY (id)
    ) DISTSTYLE AUTO SORTKEY (id);
"""

# 执行 SQL 创建表格
