### configure_redis.pp: install redis client, and redis server.
###
### Note: the prefix 'package::', corresponds to a puppet convention:
###
###       https://github.com/jeff1evesque/machine-learning/issues/2349
###

## install redis client
include package::redis_client

## install redis-server
include package::redis_server