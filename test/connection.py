#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 

import sys
from os.path import abspath, dirname, normpath, join
PREFIX = normpath(dirname(abspath(__file__)))
print "PREFIX: ", PREFIX
sys.path.insert(0, join(PREFIX, '../lib'))

from twisted.internet import protocol, reactor, defer
from rpc import GeminiRPCProtocol



class ConnectorCreator(protocol.ClientCreator):
    def __init__(self, service, *args, **kwargs):
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
def service_login(p, args):
    data = yield p.call('login', args)
    print "login p: ", p, "args: ", args
    print "login return data: ", data, type(data)
    defer.returnValue(0)

@defer.inlineCallbacks
def join_pvp(p, args):
    error, data = yield p.call('joinPVP', args)
    print "login p: ", p, "args: ", args
    print "error: ", error
    print "login return data: "
    for _key in data.keys():
        print '\t', _key, len(data[_key])
    defer.returnValue(0)

def errback(error):
    print "error: ", error

def finish(sgn):
    reactor.stop()


HOST = '120.26.229.89' #'127.0.0.1'
PORT = 12010

def connectServer():
    conn = ConnectorCreator(service_login)
    d = conn.connect(HOST, PORT)
    print 'init d: ', d

    #args = ['kkkkkkk']
    #d.addCallbacks(service_login, errback, (args,))
    args = ''
    d.addCallbacks(join_pvp, errback, (args,))
    d.addCallback(finish)


if __name__ == "__main__":
    reactor.callWhenRunning(connectServer)
    print "reactor running ..."
    reactor.run()

