#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 

from log import log
from constant import *
from manager.pvproom import PVPRoom




class PVPServer(object):
    def __init__(self):
        self.__rooms = dict()
        # just use to joinRoom function
        self.__curr_room = None

    def joinRoom(self, uid):
        '''
        @return: all balls in current room.
        '''
        if not self.__curr_room:
            _room_id = len(self.__rooms) + 1
            self.__curr_room = PVPRoom(_room_id)
            self.__rooms[_room_id] = self.__curr_room
 
        ball_data = self.__curr_room.newUser(uid)
        if self.__curr_room.count >= MAX_ROOM_COUNT:
            self.__curr_room = None

        return ball_data

    def curr_room_id(self):
        return self.__curr_room.room_id 

    def disbandRoom(self):
        pass

    def syncUserball(self):
        pass

    def syncSpingball(self):
        pass

    def updateFoodball(self):
        pass


g_PVPServer = PVPServer()
