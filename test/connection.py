#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 

import time
import sys
from os.path import abspath, dirname, normpath, join
PREFIX = normpath(dirname(abspath(__file__)))
print "PREFIX: ", PREFIX
sys.path.insert(0, join(PREFIX, '../lib'))

from twisted.internet import protocol, reactor, defer
from rpc import GeminiRPCProtocol



class ConnectorCreator(protocol.ClientCreator):
    def __init__(self, service, *args, **kwargs):
        print('------------RPC init. args:{0}, kwargs:{1}'.format(args, kwargs))
        self.factory = service
        protocol.ClientCreator.__init__(self, reactor, GeminiRPCProtocol, *args, **kwargs)

    def connect(self, host, port, timeout = 30):
        return self.connectTCP(host, port, timeout = timeout).addCallbacks(self.callback, self.errback)

    def callback(self, p):
        p.factory = self.factory
        return p

    def errback(self, error):
        print("Can't connect Server!", error)

@defer.inlineCallbacks
def funcHandlers(p, func, args):
    print "login p:", p, ", p.uid:", p.uid, ", func:", func, ", args:", args
    error, data = yield p.call(func, args)
    print "error: ", error
    if isinstance(data, dict):
        for _k, _v in data.iteritems():
            print _k, ': ', _v
    else:
        print "login return data: ", data
    defer.returnValue(0)

def errback(error):
    print "error: ", error

def finish(sgn):
    reactor.stop()


HOST = '120.26.229.89' #'127.0.0.1'
PORT = 12010

func_handlers = {
        1: ('login', ['kkkkkkk']),
        2: ('joinPVP', [3]),
        3: ('syncUserball', [(3, 1, 9849, 0, -1731, 100, 8, 0)]),
        4: ('room_ranklist', [39]),
        5: ('world_ranklist', []),
        'q': 'quit',
        'e': 'exit',
        }


def connectServer():
    #handler_id = int(sys.argv[1])
    for _k, _v in func_handlers.iteritems():
        print '    ', _k, ': ', _v
    handler_id = raw_input('Please input the number: ')
    if handler_id in ('q', 'e'):
        reactor.stop()
        return

    while True:
        try:
            handler_id = raw_input('Please input the number: ')
            handler_id = int(handler_id)
            if handler_id in func_handlers:
                break
            else:
                print "fail args ........"
        except Exception as e:
            print "fail args ........"

    conn = ConnectorCreator('')
    d = conn.connect(HOST, PORT)
    print 'init d: ', d

    func_name, args = func_handlers[handler_id]
    print('func_name:{0}, args:{1}.'.format(func_name, args))
    if func_name:
        d.addCallbacks(funcHandlers, errback, (func_name, args,))

    d.addCallback(finish)


if __name__ == "__main__":
    reactor.callWhenRunning(connectServer)
    print "reactor running ..."
    reactor.run()

