import pymysql

# Database connection parameters
db_params = {
    'host': 'your_host_name',
    'user': 'your_user_name',
    'password': 'your_username',
    'database': 'your_password',
    'port': port_number
}

# Connect to the MySQL server
conn = pymysql.connect(**db_params)

try:
    with conn.cursor() as cursor:
        batch_size = 20000

        # 這邊使用批量insert 避免產生較大的binlog 會有主從延遲的問題
        # 獲取 anonymous_user 表中的最大 ID
        cursor.execute("SELECT MAX(id) FROM anonymous_user")
        max_id_in_table = cursor.fetchone()[0]

        current_max_id = 0

        while current_max_id < max_id_in_table:
            next_max_id = current_max_id + batch_size

            insert_query = '''
            insert ignore core_user_muserlogindevice_bak0104 SELECT core_user_muserlogindevice.*
            FROM core_user_muserlogindevice JOIN anonymous_user ON core_user_muserlogindevice.user_id = anonymous_user.user_id
            WHERE anonymous_user.id >= %s AND anonymous_user.id < %s;
            '''
            cursor.execute(insert_query, (current_max_id, next_max_id))
            conn.commit()

            current_max_id = next_max_id

finally:
    conn.close()
