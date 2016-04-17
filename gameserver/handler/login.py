#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 

from twisted.internet import defer

from rpc import route
from log import log
from manager.character import Character


@route()
def login(p, req):
    log.debug("client: ", p)
    log.debug("req: ", req)
    machine_code = req
    #character_mgr = Character()
    return 0, 'test success'
