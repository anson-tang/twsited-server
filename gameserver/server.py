#!/usr/bin/env python
#-*-coding: utf-8-*-

from os.path                   import abspath, dirname
from twisted.internet.protocol import ServerFactory
from twisted.internet          import protocol, reactor, defer

from rpc                       import GeminiRPCProtocol, load_all_handlers

from log                       import log

class Server(ServerFactory):
    protocol = GeminiRPCProtocol

    def startFactory(self):
        print '=============================\n'
        print '*   Game Server Start!   *\n'
        print '============================='
        load_all_handlers(dirname(abspath(__file__)) + '/', 'handler')
 
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
