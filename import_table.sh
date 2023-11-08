#!/bin/bash

# your dump file 
# if you only want one table dump file not use all of them you can use this command to filter which table you need to use


grep -n "Table structure for table" apple_2023-11-06.sql | awk 'NR > 1 { print prev } { prev = $0 }'



## and get the start line and end line , you can create and new dump file 

sed -n 'start_line,end_line p' dump.sql > after_data.sql
