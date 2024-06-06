#!/bin/bash

key_name="g_u_b:49404132"
temp_key_name="temp_${key_name}"
hostname="localhost"
port="6379"
db=1

# Dump the key
start_dump=$(date +%s.%N)
redis-cli -h ${hostname} -p ${port} -n ${db} --raw DUMP "${key_name}" | head -c-1 > "${key_name}".bin
end_dump=$(date +%s.%N)
dump_time=$(echo "scale=3; ($end_dump - $start_dump)" | bc -l)

# Restore the key
start_restore=$(date +%s.%N)
cat "${key_name}".bin | redis-cli -h ${hostname} -p ${port} -n ${db} -x RESTORE "${temp_key_name}" 0
end_restore=$(date +%s.%N)
restore_time=$(echo "scale=3; ($end_restore - $start_restore)" | bc -l)

# Print the execution times
echo "Dump time: ${dump_time} seconds"
echo "Restore time: ${restore_time} seconds"
