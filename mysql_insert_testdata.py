import pymysql
import random

# db connection setting
config = {
    'host': 'apple-test.c7gcnnsqylcp.ap-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'k3IV7K9cQcZCqfL42TW0',
    'db': 'apple',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# connect to database
connection = pymysql.connect(**config)

def insert_batch(cursor, batch_size):
    """插入一批数据"""
    insert_sql = "INSERT INTO test_data (name, name1, name2, sex) VALUES (%s, %s, %s, %s)"
    batch_data = []
    for _ in range(batch_size):
        name = "Name_" + str(random.randint(0, 999999)).zfill(6)
        name1 = "Name1_" + str(random.randint(0, 999999)).zfill(6)
        name2 = "Name2_" + str(random.randint(0, 999999)).zfill(6)
        # random data percentage Male 45 % Female 45% Others 10%
        sex = random.choices(['M', 'F', 'Others'], weights=[45, 45, 10], k=1)[0]
        batch_data.append((name, name1, name2, sex))

    cursor.executemany(insert_sql, batch_data)
