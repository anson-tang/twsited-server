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
from manager.pvpserver import g_PVPServer



@route()
def joinPVP(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
        uid, = req

    #user = g_UserMgr.getUserBYUid(uid)
    #if not user:
    #    return CONNECTION_LOSE, None

    _u, _f, _s = g_PVPServer.joinRoom(uid)
    return NO_ERROR, dict(userball=_u, foodball=_f, spineball=_s)


@route()
def syncUserball(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
    # ball_info = [ball_id, ball_x, ball_y, ball_z, ball_r]
    ball_info, uid = req

    #user = g_UserMgr.getUserBYUid(uid)
    #if not user:
    #    return CONNECTION_LOSE, None

    room_obj = g_PVPServer.getRoomByUid(uid)
    if not room_obj:
        return PVPROOM_LOSE, None

    room_obj.syncUserBall(uid, ball_info)


@route()
def syncSpineball(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
    ball_args, uid = req

    #user = g_UserMgr.getUserBYUid(uid)
    #if not user:
    #    return CONNECTION_LOSE, None


