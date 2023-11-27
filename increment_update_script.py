import pymysql
import math

# 數據庫配置
db_config = {
    'host': 'your_host_name',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'database_name'
}

# 設置的總數量和每批處理的大小
total_count = 30000000  # 這次嘗試更新的總數量（约3000萬）
batch_size = 5000       # 每批處裡的行數
start_id = 0 # 手動指定的起始ID

# 建立連接
connection = pymysql.connect(**db_config)

try:
    with connection.cursor() as cursor:
        # 如果未指定start_id，則查詢最小的ID
        if start_id == 0:
            cursor.execute("SELECT MIN(id) FROM xxxx  WHERE tip_post_commission_percentage = 0.1")
            start_id = cursor.fetchone()[0]

        # 計算需要處理的批次數
        num_batches = math.ceil(total_count / batch_size)

        for i in range(num_batches):
            current_start_id = start_id + i * batch_size
            current_end_id = current_start_id + batch_size
                      # 執行更新
            update_query = f"""
            UPDATE xxxxxx
            SET tip_post_commission_percentage = 0
            WHERE id >= {current_start_id} AND id < {current_end_id} AND tip_post_commission_percentage = 0.1
            """
            cursor.execute(update_query)
            affected_rows = cursor.rowcount
            connection.commit()

            print(f"第{i}批處理完成，影響行数：{affected_rows}")
finally:
    connection.close()
