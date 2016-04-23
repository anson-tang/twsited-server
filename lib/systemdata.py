#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Don Li <donne.cn@gmail.com>
# License: Copyright(c) 2012 Don.Li
# Summary: 

import MySQLdb
import traceback

from log import log
from setting import DB_CONF
from constant import *



def ball_data_handler(table, fields, dataset):
    data = dict()
    for row in dataset:
        data[row[0]] = row

    return data



def randname_data_handler(table, fields, dataset):
    data = [[], []]

    for row in dataset:
        _first_name, _index = row[1:]
        if _first_name:
            data[0].append(_first_name)
        if _index:
            data[1].append(_index)

    return data


TABLES = (
        (FOR_ALL, 'foodball', ('BallId', 'BallX', 'BallY', 'BallZ'), None, ball_data_handler),
        (FOR_ALL, 'spineball', ('BallId', 'BallX', 'BallY', 'BallZ'), None, ball_data_handler),
    )





def db_config():
    return {'host'       : DB_CONF['host'],
            'port'       : DB_CONF['port'],
            'user'       : DB_CONF['user'],
            'passwd'     : DB_CONF['pass'],
            'db'         : DB_CONF['sysconfigdb'],
            'charset'    : 'utf8',
            'use_unicode': True
        }

def load_all_config(limit=FOR_ALL):
    conn   = MySQLdb.connect(**db_config())
    SELECT = 'SELECT {0} FROM tb_{1}'
    result = {}
    
    for _limit, table, fields, custom_sql, custom_handler in TABLES:
        if _limit not in (FOR_ALL, limit):
            continue

        cursor = conn.cursor()
        try:
            data = {}

            _sql = custom_sql if custom_sql else SELECT.format(','.join(fields), table)

            cursor.execute(_sql)
            _dataset = cursor.fetchall()

            if custom_handler:
                data = custom_handler(table, fields, _dataset)
            else:
                for row in _dataset:
                    if row:
                        #data[row[0]] = row
                        data[row[0]] = dict(zip(fields, row))

            result[table] = data
        except Exception, e: 
            log.warn('error sql: %s' % _sql) 
            traceback.print_exc()
            continue

        cursor.close()

    conn.close()

    result.update({'constants':constant_data()})  
    return result

def load_all_keyword():
    conn   = MySQLdb.connect(**db_config())
    cursor = conn.cursor()

    result = {}
    fields = 'k', 'v'

    sql    = 'SELECT lang_id FROM tb_lang'
    cursor.execute( sql )
    all_lang = [str(lang_id) for lang_id in cursor.fetchall()]
    all_lang.append('0')

    for lang in all_lang:
        _table_name = 'tb_keyword_%s' % lang if lang != '0' else 'tb_keyword'
        sql         = 'SELECT %s FROM %s' % (','.join(fields), _table_name)
        cursor.execute( sql )

        result[lang] = {k:v for k, v in cursor.fetchall()}

    cursor.close()
    conn.close()

    return result

def load_all_randname():
    conn   = MySQLdb.connect(**db_config())
    cursor = conn.cursor()

    result = {}
    fields = 'ID', 'FirstName', 'Index'

    _table_name = 'tb_randname'
    sql         = 'SELECT %s FROM %s' % (','.join(fields), _table_name)

    cursor.execute( sql )

    _dataset = cursor.fetchall()
    result   = randname_data_handler(_table_name, fields, _dataset)

    cursor.close()
    conn.close()

    return result

def constant_data():
    constant_data = {
            'FOODBALL_RADIUS': FOODBALL_RADIUS,
            'SPINEBALL_RADIUS': SPINEBALL_RADIUS,
            'USERBALL_RADIUS': USERBALL_RADIUS,
            'COMMON_RADIUS': COMMON_RADIUS,
            'RADIUS_EXPAND': RADIUS_ENLARGE,
            'COORDINATE_ENLARGE': COORDINATE_ENLARGE,
        }
    return constant_data

if __name__ == '__main__':
    print db_config()
    sysconfig = load_all_config()
    #print 'sysconfig:', sysconfig

    scene = repr(sysconfig['scene'][101]['Name'])
    print scene
