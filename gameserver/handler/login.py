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
from redis_constant import *
from systemdata import constant_data
from manager.character import Character
from manager.gameuser import g_UserMgr


@route()
@defer.inlineCallbacks
def login(p, req):
    log.debug("client: ", p)
    log.debug("req: ", req)
    machine_code, = req
    if not machine_code:
        defer.returnValue((MACHINE_CODE_ERROR, {}))

    uid = yield redis.hget(HASH_MACHINE_CODE_REGISTERED, machine_code)
    info = dict()
    # 创建新玩家
    if not uid:
        #TODO random nickname
        nickname = machine_code
        character_mgr = Character(0, machine_code, nickname)
        uid = character_mgr.uid
        yield character_mgr.new(machine_code, nickname)
        yield redis.hset(HASH_NICKNAME_REGISTERED, nickname, uid)
        yield redis.hset(HASH_MACHINE_CODE_REGISTERED, machine_code, uid)
        info = character_mgr.info()
    else:
        # 检查已登录时, 释放旧的连接 提示有重复登陆
        user = g_UserMgr.getUserLogined(uid, p)
        if not user:
            nickname = yield redis.hget(HASH_NICKNAME_REGISTERED, uid)
            character_mgr = Character(uid, machine_code, nickname)
            yield character_mgr.load()
            user = g_UserMgr.loginUser(p, uid, machine_code, nickname, character_mgr)
        if user:
            info = user.character_mgr.info()

    info.update({'constants':constant_data()})
    defer.returnValue((0, info))
