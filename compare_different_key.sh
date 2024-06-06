#!/bin/bash

key_name="g_u_b:49404132"
temp_key_name="temp_${key_name}"
hostname="localhost"
port="6379"
db=1

# create  compare_zsets.lua file
echo 'local old_key = KEYS[1]
local new_key = KEYS[2]

-- get old_key all of elements and score
local old_elements = redis.call("ZRANGE", old_key, 0, -1, "WITHSCORES")

-- get new_key all of elements and score
local new_elements = redis.call("ZRANGE", new_key, 0, -1, "WITHSCORES")

local old_map = {}
local new_map = {}
local differences = {}

-- let old_elements transfer to hash table
for i = 1, #old_elements, 2 do
    local member = old_elements[i]
    local score = old_elements[i + 1]
    old_map[member] = score
end

-- let new_elements transfer to hash table and find the different
for i = 1, #new_elements, 2 do
    local member = new_elements[i]
    local score = new_elements[i + 1]
    new_map[member] = score
    if old_map[member] == nil then
        table.insert(differences, member)
        table.insert(differences, score)
    end
end


-- Find elements that are present in old_key but not in new_key
for i = 1, #old_elements, 2 do
    local member = old_elements[i]
    local score = old_elements[i + 1]
    if new_map[member] == nil then
        table.insert(differences, member)
        table.insert(differences, score)
    end
end

local num_differences = #differences / 2

-- return different elements and all rows
return {num_differences, unpack(differences)}' > compare_zsets.lua

# use Redis CLI command Lua script
response=$(redis-cli -h ${hostname} -p ${port} -n ${db} --eval compare_zsets.lua "${key_name}" "${temp_key_name}")

# print different rows
num_differences=$(echo $response | awk '{print $1}')
echo "different all rows: $num_differences"

# print different elements and score
differences=$(echo $response | awk '{for(i=2;i<=NF;i++)print $i}')
echo "different elements and score :"

if [ "$num_differences" -eq 0 ]; then
  echo "Data is consistent, renaming keys..."
  redis-cli -h ${hostname} -p ${port} -n ${db} RENAME "${key_name}" "${key_name}_old"
  redis-cli -h ${hostname} -p ${port} -n ${db} RENAME "${temp_key_name}" "${key_name}"
  echo "Keys renamed successfully."
else
  echo "Data is not consistent, no renaming performed."
fi

# use while loop and read differences each elements , and create ZADD command
temp_file=$(mktemp)
count=0
while read -r member score; do
    echo "value: $member, score: $score"
    echo "ZADD ${temp_key_name} $score $member" >> $temp_file
    count=$((count+1))
done <<EOF
$(echo $differences | tr ' ' '\n' | paste - -)
EOF

# print ZADD command
echo "ADD ZADD command :"
cat $temp_file

# delete temp file 
rm -f $temp_file
