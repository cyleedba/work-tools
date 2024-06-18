import pymysql

# Database connection parameters
db_params = {
    'host': 'your_host_name',
    'user': 'username',
    'password': 'your_password',
    'database': 'database_name',
    'port': 3306
}

# Connect to the MySQL server
conn = pymysql.connect(**db_params)

try:
    with conn.cursor() as cursor:
        batch_size = 20000

        # 獲取 anonymous_user 表中的最大 ID
        cursor.execute("SELECT MAX(id) FROM anonymous_user")
        max_id_in_table = cursor.fetchone()[0]

        current_max_id = 0

        while current_max_id < max_id_in_table:
            next_max_id = current_max_id + batch_size

            # 這邊用的是join 的方式而不是子查詢的方式 子查詢 也可以用這種方式來刪除 delete from core_user_muserlogindevice where user_id in ( select user_id from anonymous_user ) limit %s offset %s 
            # 但因為資料量大當偏移量大到一定時query 在執行上會變很慢 才改用 delete from  join 的方式來實現
          
            delete_query = '''
            DELETE core_user_muserlogindevice
            FROM core_user_muserlogindevice JOIN anonymous_user ON core_user_muserlogindevice.user_id = anonymous_user.user_id
            WHERE anonymous_user.id >= %s AND anonymous_user.id < %s;
            '''
            cursor.execute(delete_query, (current_max_id, next_max_id))
            conn.commit()

            current_max_id = next_max_id

finally:
    conn.close()
