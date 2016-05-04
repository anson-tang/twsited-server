#!/usr/bin/env python
#-*-coding: utf-8-*-

from time import time
from twisted.internet import reactor, defer
from constant import *
from errorno  import *
from log import log

class GameUser(object):
    '''
    @summary: ...
    @param temp_lost:True-offline, False-online. used to 5min check. when it's status is False, don't kick it.
    '''
    def __init__(self, uid, machine_code, nickname, character_mgr):
        self.uid = uid
        self.machine_code = machine_code
        self.nickname = nickname
        self.character_mgr = character_mgr
        self.p = None
        #If user login or reconnect failure, set it to True!
        self.temp_lost = False
        # user logout's end timestamp, set a flag one-to-one of reactor logoutUserReal. 
        self.logout_timestamp = 0

    @property
    def attrib(self):
        return self.character_mgr.attrib


class GameUserMgr(object):
    def __init__(self):
        self.all_users = {} #Key is uid
        # 同时在线的最高人数
        self.max_cnt = 0

    @property
    def online_cnt(self):
        ''' used to query. '''
        return len(self.all_users)

    def online_uids(self):
        ''' used to query. '''
        return self.all_users.keys()

    def connect_uids(self):
        ''' 保持连接的玩家id列表 '''
        _uids = []
        for _user in self.all_users.values():
            if (not _user.temp_lost):
                _uids.append( _user.uid )
        return _uids

    def all_users(self):
        '''
        @summary: 返回temp_lost为False即还在线的在线玩家,用于广播, 其中不含五分钟的玩家, 
        '''
        online_users = []
        for _user in self.all_users.values():
            if (not _user.temp_lost):
                online_users.append( _user )
        return online_users

    def room_users(self, uids):
        ''' 部分玩家信息
        '''
        _room_users = []
        for uid in uids:
            _user = self.all_users.get( uid, None )
            if _user and (not _user.temp_lost):
                _room_users.append( _user )
        return _room_users

    def addUserByUser(self, user):
        if 0 == user.uid:
            return False

        if user.uid in self.all_users:
            return False
        self.all_users[user.uid] = user
        # 更新最高同时在线人数
        _total = len(self.all_users)
        if _total > self.max_cnt:
            self.max_cnt = _total
        return True

    def getUserByUid(self, uid):
        if uid in self.all_users:
            return self.all_users[uid]
        else:
            return None

    def delUserByUid(self, uid):
        user = self.all_users.get(uid, None)
        if user:
            del self.all_users[uid]
            return True
        else:
            return False

    def getUserLogined(self, uid, p):
        user = self.all_users.get(uid, None)
        if user:
            if hasattr(user, 'p') and user.p and user.p.transport:
                try:
                    user.p.lose_connect = False
                    user.p.transport.loseConnection()
                except Exception, e:
                    log.error('exception. uid: {0}, e: {1}.'.format( uid, e ))

            user.p = p
            p.uid  = user.uid
            user.temp_lost = False
            user.logout_timestamp = 0
            log.warn('Replace old client. uid: {0}.'.format( p.uid ))

        return user

    def loginUser(self, p, uid, machine_code, nickname, character_mgr):
        user = None
        if uid in self.all_users:
            user = self.all_users[uid]
        else:
            user = GameUser(uid, machine_code, nickname, character_mgr)
        user.p = p

        p.uid = uid
        log.debug('uid:{0}, machine_code:{1}, all_users:{2}'.format( uid, machine_code, self.all_users ))
        user.temp_lost = False
        user.logout_timestamp = 0

        if uid != 0:
            self.addUserByUser(user)

        return user

    def logoutUser(self, uid):
        user = self.all_users.get(uid, None)

        if user:
            user.p = None
            user.temp_lost = True
            # update logout_timestamp
            now_timestamp  = int(time())
            user.logout_timestamp = now_timestamp
 
            reactor.callLater(SESSION_LOGOUT_REAL,  self.logoutUserReal, uid, now_timestamp)
            log.debug('user will logout later. uid: {0}.'.format( uid ))
        else:
            log.warn('Unknown user. uid: {0}.'.format( uid ))

    def reconnectUser(self, p, uid):
        user = self.all_users.get(uid, None)
        if user:
            #if  user.session_key != session_key:
            #    log.error('Session not match. old sk: {0}, new sk:{1}.'.format( user.session_key, session_key ))
            #    return RECONNECT_FAIL
            #if False == user.temp_lost:
            #    log.error('It is not temp lost client. uid:', user.uid)
            #    return CONNECTION_LOSE

            # check old protocol is valid or not.
            old_p = user.p
            user.p = None
            if old_p:
                old_p.lose_connect = True
                if hasattr(old_p, 'uid') and old_p.uid:
                    old_p.uid = 0
                if old_p.transport:
                    old_p.transport.loseConnection()

            user.p = p
            user.uid = user.uid
            user.machine_code = user.machine_code
            user.nickname = user.nickname
            user.temp_lost = False
            user.logout_timestamp = 0

            log.info('Reconnect ok. uid: {0}, lose_connect: {1}.'.format( p.uid, p.lose_connect ))
            return NO_ERROR
        else:
            log.error('Can not find uid: {0}.'.format( uid ))
            return CONNECTION_LOSE

    @defer.inlineCallbacks
    def logoutUserReal(self, uid, now_timestamp):
        ''' 同时满足两个条件才能真正的删除玩家
           1: temp_lost == True, offline
           2: logout_timestamp == now_timestamp, 借用时间戳作为标识, 匹配后标识是同一个事件
        '''
        user = self.all_users.get(uid, None)
        if user:
            log.debug('logout uid: {0}, temp_lost: {1}, logout_timestamp: {2}, now_timestamp: {3}.'.format(\
                    uid, user.temp_lost, user.logout_timestamp, now_timestamp) )
            if user.temp_lost and user.logout_timestamp == now_timestamp:
                self.delUserByUid( uid )
                log.debug('User logout real. uid: {0}.'.format( uid ))
        else:
            log.error('User had logout. uid: {0}.'.format( uid ))

    @defer.inlineCallbacks
    def del_zombie_user(self, uid):
        ''' 清除僵尸玩家，无效client连接
        '''
        _user = self.all_users.get(uid, None)
        if _user:
            if hasattr(_user, 'p'):
                if hasattr(_user.p, 'transport'):
                    if _user.p.transport:
                        defer.returnValue( NO_ERROR )
                    else:
                        log.error('Unknown user. uid:{0}, transport:{1}.'.format(uid, _user.p.transport))
                else:
                    log.warn('Unknown user. uid:{0}, the p has no transport attribute..'.format(uid))
            else:
                log.warn('__broadcast. uid:{0}, the user has no p attribute..'.format(_user.uid))

            self.delUserByUid( uid )
            log.warn('Del zombie user success. uid: {0}.'.format( uid ))
        defer.returnValue( NO_ERROR )

    def loseConnection(self, uid):
        user = self.all_users.get(uid, None)
        if user:
            if hasattr(user, 'p') and user.p and user.p.transport:
                try:
                    user.p.transport.loseConnection()
                except Exception, e:
                    log.error('exception. uid: {0}, e: {1}.'.format( uid, e ))
            log.warn('Lose connection user success. uid: {0}.'.format( uid ))
        else:
            log.error('Unknown user. uid: {0}.'.format( uid ))
 
    @defer.inlineCallbacks
    def kickoutUser(self, uid):
        _user = self.all_users.get(uid, None)
        if _user:
            self.delUserByUid( uid )

        defer.returnValue( NO_ERROR )

g_UserMgr = GameUserMgr()
