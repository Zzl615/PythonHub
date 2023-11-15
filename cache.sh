redis-cli -h 211.154.163.95 -p 6379 KEYS "gouhuo_*"

redis-cli -h 211.154.163.95 -p 6379 KEYS "gouhuo_*"|xargs redis-cli -h 211.154.163.95 -p 6379 DEL