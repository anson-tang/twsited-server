#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 

import sys, os
if sys.getdefaultencoding != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
import random
import math
import MySQLdb

from os.path import abspath, dirname, join, normpath
PREFIX = normpath(dirname(abspath(__file__)))
print "PREFIX: ", PREFIX
for path in (PREFIX, normpath(join(PREFIX, '../lib'))):
    if path not in sys.path:
        sys.path = [path] + sys.path

from log import log
from setting import DB_CONF
from systemdata import TABLES, db_config
from constant import *



def insert_mysql(table, values):
    conn   = MySQLdb.connect(**db_config())
    cursor = conn.cursor()
    del_sql = 'TRUNCATE TABLE tb_%s;' % table
    cursor.execute(del_sql)

    fields = ''
    for _line in TABLES:
        if _line[1] == table:
            fields = _line[2]
    if not fields:
        return

    insert_sql = 'INSERT INTO tb_%s (' % table + ','.join(fields) + ') VALUES ('  + ','.join(['%s'] * len(fields)) + ')'
    cursor.executemany(insert_sql, values)
    #print('=========sql: {0}'.format(insert_sql))
    #print('=========values: {0}'.format(values))
    conn.commit()

    cursor.close()
    conn.close()



def init_ball_data(table, count):
    if not (table and count):
        print "fail............."
        return

    try:
        values = list()
        radius = COMMON_RADIUS * COORDINATE_ENLARGE / RADIUS_ENLARGE
        for i in xrange(1, count+1):
            y = random.randint(-radius, radius)
            max_z = int(math.sqrt(radius**2 - y**2))
            z = random.randint(-max_z, max_z)
            x = random.choice((-1, 1)) * int(math.sqrt(radius**2 - y**2 - z**2))
            values.append((i,x,y,z))

        insert_mysql(table, values)
    except Exception as e:
        print "error: ", e
        print "radius:%s, count:%s, x:%s, y:%s, z:%s." % (radius, count, x, y, z)



if __name__ == "__main__":
    # init foodball data
    init_ball_data('foodball', 1000)

    # init foodball data
    init_ball_data('spineball', 20)
