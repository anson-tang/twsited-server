#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 
from twisted.internet import defer

from rpc import route
from log import log
from constant import *
from errorno import *
from manager.gameuser import g_UserMgr


@route()
@defer.inlineCallbacks
def room_ranklist(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
        uid = 3
        defer.returnValue((CONNECTION_LOSE, None))

    user = g_UserMgr.getUserByUid(uid)
    if not user:
        defer.returnValue((CONNECTION_LOSE, None))

    room_obj = g_PVPServer.getRoomByUid(uid)
    if not room_obj:
        defer.returnValue((PVPROOM_LOSE, None))

    # rank, uid, machine_code, weight, eat_num, be_eated_num
    err, data = yield room_obj.finalRanklist()
    defer.returnValue((err, data))
