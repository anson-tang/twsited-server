#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 
import random
import math

from twisted.internet import defer
from rpc import route
from log import log
from constant import *
from errorno import *
from manager.gameuser import g_UserMgr
from manager.pvpserver import g_PVPServer



@route()
@defer.inlineCallbacks
def joinPVP(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
        defer.returnValue((CONNECTION_LOSE, None))

    user = g_UserMgr.getUserByUid(uid)
    if not user:
        defer.returnValue((CONNECTION_LOSE, None))

    data = yield g_PVPServer.joinRoom(uid)
    log.warn('==============joinPVP userball:{0}'.format(data['userball']))
    defer.returnValue((NO_ERROR, data))


@route()
@defer.inlineCallbacks
def syncUserball(p, req):
    '''
    @req: [[uid, ball_id, ball_x, ball_y, ball_z, ball_r, volume, speed], ......]
    '''
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
        defer.returnValue((CONNECTION_LOSE, None))

    log.warn('==============req:{0}.'.format(req))
    user = g_UserMgr.getUserByUid(uid)
    if not user:
        defer.returnValue((CONNECTION_LOSE, None))

    room_obj = g_PVPServer.getRoomByUid(uid)
    if not room_obj:
        defer.returnValue((PVPROOM_LOSE, None))

    err, data = yield room_obj.syncUserball(user.attrib, req)
    defer.returnValue((err, data))


@route()
def syncSpineball(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        log.error('client has not found uid.')
        return(CONNECTION_LOSE, None)

    user = g_UserMgr.getUserByUid(uid)
    if not user:
        return(PVPROOM_LOSE, None)

    room_obj = g_PVPServer.getRoomByUid(uid)
    if not room_obj:
        return(PVPROOM_LOSE, None)

    err, data = room_obj.syncSpineball(uid, req)
    return(err, data)


