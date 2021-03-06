#!/usr/bin/env python
#-*-coding: utf-8-*-

import MySQLdb
import setting

from os.path import abspath, dirname
from twisted.internet.protocol import ServerFactory
from twisted.internet import protocol, reactor, defer

from rpc import GeminiRPCProtocol, load_all_handlers
from redis import redis
from log import log
from redis_constant import *



class Server(ServerFactory):
    protocol = GeminiRPCProtocol

    def startFactory(self):
        print '=============================\n'
        print '*   Game Server Start!   *\n'
        print '============================='
        load_all_handlers(dirname(abspath(__file__)) + '/', 'handler')

        self.__migrate_accounts_registered()

    @defer.inlineCallbacks
    def __migrate_accounts_registered(self):
        try:
            yield redis.delete(HASH_NICKNAME_REGISTERED, HASH_MACHINE_CODE_REGISTERED, HASH_UID_MACHINE_CODE, SET_RANK_PVP_WEIGHT)

            db_conf = {'host': setting.DB_CONF['host'],
                'port'       : setting.DB_CONF['port'],
                'user'       : setting.DB_CONF['user'],
                'passwd'     : setting.DB_CONF['pass'],
                'db'         : setting.DB_CONF['userdb'],
                'charset'    : 'utf8'
                }

            conn = MySQLdb.connect(**db_conf)
            cu   = conn.cursor()

            cu.execute('SELECT `id`,`machine_code`,`nickname`,`max_weight` FROM tb_character')
            _dataset = cu.fetchall()
            for _id, _machine_code, _nickname, _max_weight in _dataset:
                yield redis.hset(HASH_NICKNAME_REGISTERED, _nickname, _id)
                yield redis.hset(HASH_MACHINE_CODE_REGISTERED, _machine_code, _id)
                yield redis.hset(HASH_UID_MACHINE_CODE, _id, _machine_code)
                yield redis.zadd(SET_RANK_PVP_WEIGHT, _id, -_max_weight)

            cu.close()
            conn.close()

            conn = None
            cu   = None
        except Exception, e:
            reactor.callLater(1, self.__migrate_accounts_registered)
            print 'ERROR:', e
            print 'WARNING. Redis connection fail, callLater 1 second. redis:', redis

 
    def cleanup(self):
        pass

    def stopFactory(self):
        print '=============================\n'
        print '*  Game Server Stop!     *\n'
        print '============================='

        try:
            pass
        except:
            log.exception()
