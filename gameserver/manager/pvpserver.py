#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 

from twisted.internet import defer
from log import log
from constant import *
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
        if not self.__curr_room:
            # new a room
            _room_id = len(self.__rooms) + 1
            self.__curr_room = PVPRoom(_room_id)
            self.__rooms[_room_id] = self.__curr_room
 
        ball_data = yield self.__curr_room.newUser(uid)
        if self.__curr_room.count >= MAX_USER_COUNT:
            self.__curr_room = None

        defer.returnValue(ball_data)

    def curr_room_id(self):
        return self.__curr_room.room_id 

    def getRoomByUid(self, uid):
        for _room in self.__rooms.itervalues():
            if _room.isMember(uid):
                return _room
        return None

    def disbandRoom(self):
        pass


g_PVPServer = PVPServer()
