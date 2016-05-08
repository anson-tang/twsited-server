#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 

from twisted.internet import defer
from log import log
from redis import redis
from constant import *
from errorno import *
from redis_constant import *
from manager.pvproom import PVPRoom




class PVPServer(object):
    def __init__(self):
        self.__rooms = dict()
        # just use to joinRoom function
        self.__curr_room = None

    @defer.inlineCallbacks
    def joinRoom(self, uid):
        '''
        @return: all balls in current room.
        '''
        if self.__curr_room and (self.__curr_room.count >= MAX_USER_COUNT or \
                self.__curr_room.isEnd):
            del self.__rooms[self.__curr_room.room_id]
            log.error('------- curr_room.count:{0}, isEnd:{1}.'.format(self.__curr_room.count, self.__curr_room.isEnd))
            self.__curr_room = None

        if not self.__curr_room:
            # new a room and get last room_id
            _room_id = yield redis.get(STRING_LAST_ROOM_ID)
            log.error('-----_last_room_id:{0}'.format(_room_id))
            _room_id = int(_room_id) + 1 if _room_id else 1
            log.error('-----_curr_room_id:{0}'.format(_room_id))
            yield redis.set(STRING_LAST_ROOM_ID, _room_id)
            self.__curr_room = PVPRoom(_room_id)
            self.__rooms[_room_id] = self.__curr_room
 
        ball_data = yield self.__curr_room.newUser(uid)

        defer.returnValue(ball_data)

    def curr_room_id(self):
        return self.__curr_room.room_id 

    def getRoomByUid(self, uid):
        for _room in self.__rooms.itervalues():
            if not _room.isMember(uid) or _room.isEnd:
                continue
            return _room
        return None

    @defer.inlineCallbacks
    def getRoomRanklist(self, room_id, self_uid):
        other_data = list()
        _volume_data = yield redis.zrange(SET_RANK_ROOM_VOLUME%room_id, 0, 5, True)
        _volume_data = _volume_data if _volume_data else list()
        for _rank, (_uid, _volume) in enumerate(_volume_data):
            _machine_code = yield redis.hget(HASH_UID_MACHINE_CODE, _uid)
            _eat_num = yield redis.zscore(SET_RANK_ROOM_EAT%room_id, _uid)
            _eat_num = abs(int(_eat_num)) if _eat_num else 0
            _be_eated_num = yield redis.hget(SET_RANK_ROOM_EATED%room_id, _uid)
            _be_eated_num = abs(int(_be_eated_num)) if _be_eated_num else 0
            other_data.append((_rank+1, _uid, _machine_code, abs(_volume)*10, _eat_num, _be_eated_num))

        _self_rank = yield redis.zrank(SET_RANK_ROOM_VOLUME%room_id, self_uid)
        _self_rank = 0 if _self_rank is None else int(_self_rank) + 1
        _self_volume = yield redis.zscore(SET_RANK_ROOM_VOLUME%room_id, self_uid)
        _self_weight = abs(_self_volume)*10 if _self_volume else 0
        _self_machine_code = yield redis.hget(HASH_UID_MACHINE_CODE, self_uid)
        _self_eat_num = yield redis.zscore(SET_RANK_ROOM_EAT%room_id, self_uid)
        _self_eat_num = abs(int(_self_eat_num)) if _self_eat_num else 0
        _self_be_eated_num = yield redis.hget(SET_RANK_ROOM_EATED%room_id, self_uid)
        _self_be_eated_num = abs(int(_self_be_eated_num)) if _self_be_eated_num else 0
        self_data = (_self_rank, self_uid, _self_machine_code, _self_eat_num, _self_be_eated_num)

        defer.returnValue((other_data, self_data))



g_PVPServer = PVPServer()
