#!/usr/bin/env python
#-*- coding: utf-8-*-

from twisted.application     import internet, service
from twisted.internet        import reactor, protocol
from twisted.manhole.telnet  import ShellFactory
from twisted.python.log      import ILogObserver, FileLogObserver
from twisted.python.logfile  import LogFile

import sys, os
if sys.getdefaultencoding != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

from os.path import abspath, dirname, join, normpath
PREFIX = normpath(dirname(abspath(__file__)))
for path in (PREFIX, normpath(join(PREFIX, '../lib'))):
    if path not in sys.path:
        sys.path = [path] + sys.path

import setting
SERVER_NAME = 'GAMESERVER'
import log
log.init(setting.LOG_THRESHOLD)

import redis
redis.init(setting.REDIS_CONF)


from server import Server
from datetime import datetime

server = Server()
reactor.addSystemEventTrigger('before', 'shutdown', server.cleanup)
application = service.Application(SERVER_NAME)

logfile = LogFile('game.log', join(PREFIX, '../logs'), rotateLength=setting.LOG_ROTATE_INTERVAL)
logOb = FileLogObserver(logfile)
logOb.formatTime = lambda when : datetime.fromtimestamp(when).strftime('%m/%d %T.%f')
application.setComponent( ILogObserver, logOb.emit )

internet.TCPServer(setting.GAMESERVER['port'], server, interface=setting.GAMESERVER['hostname']).setServiceParent(service.IServiceCollection(application))
internet.TCPServer(setting.GAMESERVER['adminport'], ShellFactory(), interface=setting.GAMESERVER['hostname']).setServiceParent(service.IServiceCollection(application))
