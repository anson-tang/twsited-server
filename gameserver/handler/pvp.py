#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 
import random
import math

from rpc import route
from log import log
from constant import *
from errorno import *
from manager.gameuser import g_UserMgr
from manager.pvpserver import g_PVPServer



@route()
def joinPVP(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
        uid, = req
        return CONNECTION_LOSE, None

    user = g_UserMgr.getUserByUid(uid)
    if not user:
        return CONNECTION_LOSE, None

    _u, _f, _s = g_PVPServer.joinRoom(uid)
    return NO_ERROR, dict(userball=_u, foodball=_f, spineball=_s)


@route()
def syncUserball(p, req):
    '''
    @req: [[ball_id, ball_x, ball_y, ball_z, ball_r], ......]
    '''
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
        uid = 1
        return CONNECTION_LOSE, None

    user = g_UserMgr.getUserByUid(uid)
    if not user:
        return CONNECTION_LOSE, None

    room_obj = g_PVPServer.getRoomByUid(uid)
    if not room_obj:
        return PVPROOM_LOSE, None

    err, data = room_obj.syncUserball(uid, req)
    return err, data


@route()
def syncSpineball(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
        uid = 1
        return CONNECTION_LOSE, None

    user = g_UserMgr.getUserByUid(uid)
    if not user:
        return PVPROOM_LOSE, None

    err, data = room_obj.syncSpineball(uid, req)
    return err, data


