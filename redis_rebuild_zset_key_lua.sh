# 初始参数
old_key="your_key_name"
new_key="temp_${old_key}"
batch_size=2000
cursor=0

# 创建 rebuild_zset.lua 文件
echo 'local old_key = KEYS[1]
local new_key = KEYS[2]
local batch_size = tonumber(ARGV[1])
local cursor = ARGV[2]

-- 获取一批 zset 元素
local res = redis.call("ZSCAN", old_key, cursor, "COUNT", batch_size)
cursor = res[1]
local elements = res[2]

-- 将元素添加到新 zset
for i = 1, #elements, 2 do
    local member = elements[i]
    local score = elements[i + 1]
    redis.call("ZADD", new_key, score, member)
end

-- 返回新的 cursor
return cursor' > rebuild_zset.lua

# 记录开始时间
start_time=$(date +%s)

# 循环执行 Lua 脚本
while : ; do
  # 调用 redis-cli 执行 Lua 脚本，并获取返回的 cursor
  response=$(redis-cli -p 6379 -n 1 --eval rebuild_zset.lua $old_key $new_key , $batch_size $cursor)

  # 获取新的 cursor
  cursor=$(echo $response | tr -d '\r\n')

  # 打印 cursor 值，用于调试
  echo "Cursor: $cursor"

  # 检查 cursor 是否为 0，如果是则退出循环
  if [ "$cursor" -eq 0 ]; then
    break
  fi
done


# 记录结束时间
end_time=$(date +%s)


# 计算并打印耗时
elapsed_time=$((end_time - start_time))
echo "脚本执行时间: ${elapsed_time} 秒"
