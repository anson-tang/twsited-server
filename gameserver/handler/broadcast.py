#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import reactor
from rpc import route
from log import log
from constant import MAX_BROADCAST_PER_LOOP
from manager.gameuser import g_UserMgr




def send2client(uids, func, args):
    _remain = g_UserMgr.room_users(uids)
    __broadcast(_remain, func, args)


@route()
def broadcast(p, req):
    func, args = req
    _remain = g_UserMgr.all_users()
    __broadcast(_remain, func, args)

@route()
def room_broadcast(p, req):
    func, args, uids = req
    _remain = g_UserMgr.room_users( uids )
    __broadcast(_remain, func, args)

def __broadcast(user_remain, func, args):
    log.debug('================__broadcast user_remain:{0}, func:{1}, args: {2}.'.format(user_remain, func, args))
    if user_remain:
        i = 0
        while i < MAX_BROADCAST_PER_LOOP:
            i += 1
            _user = user_remain.pop( 0 )
            if _user:
                if hasattr(_user, 'p'):
                    if hasattr(_user.p, 'transport'):
                        if _user.p.transport:
                            _user.p.send(func, args)
                        else:
                            log.warn('__broadcast. cid:{0}, unknown t:{1}.'.format(_user.cid, _user.p.transport))
                            g_UserMgr.del_zombie_user( _user.cid )
                    else:
                        log.warn('__broadcast. cid:{0}, the p has no transport attribute..'.format(_user.cid))
                        g_UserMgr.del_zombie_user( _user.cid )
                else:
                    log.warn('__broadcast. cid:{0}, the user has no p attribute..'.format(_user.cid))
                    g_UserMgr.del_zombie_user( _user.cid )
            else:
                log.info('__broadcast. Unknown user.')

            if not user_remain:
                break
        else:
            reactor.callLater(1, __broadcast, user_remain, func, args)
