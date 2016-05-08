#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 
from twisted.internet import defer

from rpc import route
from log import log
from redis import redis
from constant import *
from errorno import *
from redis_constant import *
from manager.gameuser import g_UserMgr
from manager.pvpserver import g_PVPServer


@route()
@defer.inlineCallbacks
def room_ranklist(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
        defer.returnValue((CONNECTION_LOSE, None))

    user = g_UserMgr.getUserByUid(uid)
    if not user:
        defer.returnValue((CONNECTION_LOSE, None))

    room_id, = req
    data = yield g_PVPServer.getRoomRanklist(room_id, uid)

    defer.returnValue((NO_ERROR, data))


@route()
@defer.inlineCallbacks
def world_ranklist(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
        defer.returnValue((CONNECTION_LOSE, None))

    user = g_UserMgr.getUserByUid(uid)
    if not user:
        defer.returnValue((CONNECTION_LOSE, None))

    data = list()
    other_data = list()
    weight_data = yield redis.zrange(SET_RANK_PVP_WEIGHT, 0, 10, True)
    for _rank, (_uid, _weight) in enumerate(weight_data):
        _machine_code = yield redis.hget(HASH_UID_MACHINE_CODE, _uid)
        other_data.append((_rank+1, _uid, _machine_code, _weight))

    self_rank = yield redis.zrank(SET_RANK_PVP_WEIGHT, uid)
    self_rank = 0 if self_rank is None else int(self_rank) + 1
    self_machine_code = yield redis.hget(HASH_UID_MACHINE_CODE, uid)
    self_weight = yield redis.zscore(SET_RANK_PVP_WEIGHT, uid)
    self_weight = 0 if self_weight is None else abs(self_weight)

    data = (other_data, (self_rank, uid, self_machine_code, self_weight))
    defer.returnValue((NO_ERROR, data))
