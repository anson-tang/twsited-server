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
        uid = 3
        return CONNECTION_LOSE, None

    user = g_UserMgr.getUserByUid(uid)
    if not user:
        return CONNECTION_LOSE, None

    _u, _f, _s, _t, _r = g_PVPServer.joinRoom(uid)
    data = {'userball':_u, 'foodball':_f, 'spineball':_s, 'end_time':_t, 'rank':_r}
    log.warn('==============joinPVP userball:{0}'.format(_u))
    return NO_ERROR, data


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
        uid = 3
        return CONNECTION_LOSE, None

    log.warn('==============req:{0}.'.format(req))
    user = g_UserMgr.getUserByUid(uid)
    if not user:
        return CONNECTION_LOSE, None

    room_obj = g_PVPServer.getRoomByUid(uid)
    if not room_obj:
        return PVPROOM_LOSE, None

    err, data = room_obj.syncUserball(user.attrib, req)
    return err, data


@route()
def syncSpineball(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
        return CONNECTION_LOSE, None

    user = g_UserMgr.getUserByUid(uid)
    if not user:
        return PVPROOM_LOSE, None

    err, data = room_obj.syncSpineball(uid, req)
    return err, data


