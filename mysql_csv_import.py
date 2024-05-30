import csv
import pymysql

# Database connection
conn = pymysql.connect(host='xxxxxx', user='xxxx', password='xxxxx', db='xxxx')
cursor = conn.cursor()

# Function to insert batch
def insert_batch(batch_data):
    cursor.executemany('INSERT INTO anonymous_user1229(user_id, device_info, device_id) VALUES(%s, %s, %s)', batch_data)
    conn.commit()
    batch_data.clear()

# Reading CSV file
batch_size = 50000  # Number of rows per batch
batch_data = []     # Temporary list to store data

with open('/tmp/1227.csv', 'r') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Skip header row

    for row in csv_data:
        batch_data.append(row)
        if len(batch_data) >= batch_size:
            insert_batch(batch_data)

# Insert any remaining data
if batch_data:
    insert_batch(batch_data)

# Closing the connection
cursor.close()
conn.close()
