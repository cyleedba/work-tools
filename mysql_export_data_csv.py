import pymysql
import csv

# Database connection parameters
host = 'your_hostname'
port = 3306  # or your RDS port
username = 'your_username'
password = 'your_password'
database = 'your_databasename'

# 因為mysqldump 沒辦法使用join 的方式來做資料的導出 故才改使用 python 腳本來實現
# 導出後 要在import 可以使用 LOAD DATA LOCAL INFILE 的方式來匯入 
# SQL query
query = '''
SELECT a.user_id
FROM anonymous_user a ;
'''

# Connect to the database
connection = pymysql.connect(host=host, port=port, user=username, passwd=password, db=database)

try:
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

        # Write to CSV file
        with open('anonymous_user.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header (optional, uncomment the next line if you want headers)
            # writer.writerow([i[0] for i in cursor.description])
            writer.writerows(result)

finally:
    connection.close()
