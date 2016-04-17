#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Don Li <donne.cn@gmail.com>
# License: Copyright(c) 2013 Don.Li
# Summary: 

#from pyredis import Redis
#import config
#
#try:
#    redis
#except NameError:
#    redis  = Redis(**config.redis_conf)


import py_txredisapi as REDIS

redis = None

def init(conf):
    global redis

    redis_sock = conf.get('redis_sock', None)

    if redis_sock:
        redis_conf = dict(
                path = redis_sock, 
                dbid = conf['redis_db'],
                password = conf['redis_passwd']
                )
    else:
        redis_conf = dict(
                host = conf['redis_host'],
                port = conf['redis_port'],
                dbid = conf['redis_db'],
                password = conf['redis_passwd']
                )


    if not redis:
        redis = REDIS.lazyUnixConnectionPool(**redis_conf)

