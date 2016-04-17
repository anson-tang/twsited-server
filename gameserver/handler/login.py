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
from manager.character import Character


@route()
@defer.inlineCallbacks
def login(p, req):
    log.debug("client: ", p)
    log.debug("req: ", req)
    machine_code = req

    uid = yield redis.hget(HASH_MACHINE_CODE_REGISTERED, machine_code)
    # 创建新玩家
    if not uid:
        nickname = 'hiwo'
        character_mgr = Character(0, machine_code, nickname)
        uid = character_mgr.uid
        yield character_mgr.new(machine_code, nickname)
        yield redis.hset(HASH_NICKNAME_REGISTERED, nickname, uid)
        yield redis.hset(HASH_MACHINE_CODE_REGISTERED, machine_code, uid)
    else:
        # 检查已登录时, 释放旧的连接 提示有重复登陆
        old_p = g_ClientsMgr.get_client_by_uid(uid)
        if old_p:
            p.character_mgr = old_p.character_mgr
            old_p.close()
        else:
            nickname = yield redis.hget(HASH_NICKNAME_REGISTERED, uid)
            character_mgr = Character(uid, machine_code, nickname)
            yield character_mgr.load()
    g_ClientsMgr.login(p)
    defer.returnValue( 0, 'test success' )
