#!/usr/bin/env python
#-*-coding: utf-8-*-

from os.path import abspath, dirname
from twisted.internet.protocol import ServerFactory
from twisted.internet import protocol, reactor, defer

from rpc import GeminiRPCProtocol, load_all_handlers
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
            yield redis.delete( HASH_ACCOUNT_REGISTERED )
            yield redis.delete( HASH_NICKNAME_REGISTERED )
            yield redis.delete( SET_CID_REGISTERED )

            db_conf = {'host': DB['host'],
                'port'       : DB['port'],
                'user'       : DB['user'],
                'passwd'     : DB['pass'],
                'db'         : DB['db_userdb'],
                'charset'    : 'utf8'
                }

            conn = MySQLdb.connect(**db_conf)
            cu   = conn.cursor()

            cu.execute('SELECT `id`,`machine_code`,`nickname` FROM tb_character')
            _dataset = cu.fetchall()
            for _id, _machine_code, _nickname in _dataset:
                yield redis.hset(HASH_NICKNAME_REGISTERED, _nickname, _id)
                yield redis.sadd(SET_MACHINE_CODE_REGISTERED, _id)

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
