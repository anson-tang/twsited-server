#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 

import MySQLdb
import sys, os
if sys.getdefaultencoding != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

from os.path import abspath, dirname, join, normpath
PREFIX = normpath(dirname(abspath(__file__)))
print "PREFIX: ", PREFIX
for path in (PREFIX, normpath(join(PREFIX, '../lib'))):
    if path not in sys.path:
        sys.path = [path] + sys.path

from log import log
from setting import DB_CONF
from systemdata import TABLES, db_config



def insert_mysql(table, values):
    conn   = MySQLdb.connect(**db_config())
    cursor = conn.cursor()

    fields = ''
    for _line in TABLES:
        if _line[1] == table:
            fields = _line[2]
    if not fields:
        return

    sql = 'INSERT INTO tb_%s (' % table + ','.join(fields) + ') VALUES ('  + ','.join(['%s'] * len(fields)) + ')'
    cursor.executemany(sql, values)
    print('=========sql: {0}'.format(sql))
    print('=========values: {0}'.format(values))
    conn.commit()

    cursor.close()
    conn.close()

    return True

def init_ball_data():
    pass


if __name__ == "__main__":
    values = [[7, 111,123, 112],
            [8, 211, 213, 245],
            [9, 310, 392, 278],
            ]
    
    insert_mysql('foodball', values)
