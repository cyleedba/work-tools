#!/bin/bash

# 設定變量以方便修改和重用
REDIS_HOST="redis-db.bxbb5w.ng.0001.ape1.cache.amazonaws.com"
REDIS_PORT=6379
REDIS_DB_INDEX=1
LOG_FILE="redis-cli-bigkeys.log"

# 獲取當前時間戳記，用於計算執行時間
START_TIME=$(date +%s)
START_TIME_HUMAN=$(date +"%Y-%m-%d %H:%M:%S")

# 執行命令並記錄到日誌文件，包括開始執行的時間
echo "======redis-db======" | tee -a $LOG_FILE
echo "Command started at: $START_TIME_HUMAN" | tee -a $LOG_FILE
redis-cli -h $REDIS_HOST -p $REDIS_PORT -n $REDIS_DB_INDEX --bigkeys >> $LOG_FILE

# 計算並記錄執行的結束時間和持續時間
END_TIME=$(date +%s)
END_TIME_HUMAN=$(date +"%Y-%m-%d %H:%M:%S")
DURATION=$((END_TIME - START_TIME))

echo "Command ended at: $END_TIME_HUMAN" | tee -a $LOG_FILE
echo "Duration: $DURATION seconds" | tee -a $LOG_FILE
