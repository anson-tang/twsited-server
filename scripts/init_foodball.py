#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 

import MySQLdb

from log import log
from setting import DB_CONF
from systemdata import TABLES



def db_config():
    return {'host'       : DB_CONF['host'],
            'port'       : DB_CONF['port'],
            'user'       : DB_CONF['user'],
            'passwd'     : DB_CONF['pass'],
            'db'         : DB_CONF['sysconfigdb'],
            'charset'    : 'utf8',
            'use_unicode': True
        }

def init_data(table, values):
    conn   = MySQLdb.connect(**db_config())
    cursor = conn.cursor()

    fields = ''
    for _line in TABLES:
        if _line[1] == table:
            fields = _line[2]
    if not fields:
        return

    sql = 'INSERT INTO tb_%s (' % table + ','.join(fields) + ') VALUES ('  + ','.join(['%s'] * len(fields)) + ')'
    #cursor.execute( sql )
    cursor.insert(_sql, _values)
    cursor.fetchall()

    cursor.close()
    conn.close()

    return result

values = [[1, 111,123, 112],
        [2, 211, 213, 245],
        [3, 310, 392, 278],
        ]

init_data('foodball', values)
