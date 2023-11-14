#!/bin/bash

# 讓用戶輸入 dump 檔案名和想要提取的表名
echo "Enter the name of your dump file (e.g., apple_2023-11-06.sql):"
read dump_file
echo "Enter the name of the table you want to extract (e.g., core_pay_mpay):"
read table_name

# 獲取表的起始行
start_line=$(grep -n "Table structure for table \`$table_name\`" $dump_file | awk -F ':' '{print $1}')

# 獲取表的結束行
next_table_line=$(grep -n "Table structure for table" $dump_file | awk -F ':' -v start="$start_line" 'NR > 1 && $1 > start {print $1; exit}')
end_line=$((next_table_line - 1))

# 檢查是否找到起始行和結束行
if [ -n "$start_line" ] && [ -n "$end_line" ]; then
    # 使用 sed 提取表數據到新文件
    sed -n "${start_line},${end_line}p" $dump_file > "${table_name}_data.sql"
    echo "Extracted data for table '$table_name' into ${table_name}_data.sql"
else
    echo "Table '$table_name' not found in $dump_file"
fi
