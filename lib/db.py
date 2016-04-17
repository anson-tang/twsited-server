#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Don Li <donne.cn@gmail.com>
# License: Copyright(c) 2013 Don.Li
# Summary: 

import setting
from dbhelper import DBHelper

try:
    POOL
except NameError:
    print "db conf:", setting.DB_CONF
    user_db_conf = dict(
                      host     = setting.DB_CONF['host'],
                      port     = setting.DB_CONF['port'],
                      user     = setting.DB_CONF['user'],
                      passwd   = setting.DB_CONF['pass'],
                      db       = setting.DB_CONF['userdb'],
                      #charaset = 'utf8',
                      cp_noisy = setting.DEBUG,
                      cp_min   = 5,
                      cp_max   = setting.DB_CONF['pool_size'],
                      cp_reconnect = True)

    print "final db conf:", user_db_conf
    POOL = DBHelper(**user_db_conf)
    print "POOL: ", POOL
