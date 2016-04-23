#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 
import random
import math
from log import log
from system import *
from constant import *


class Userball(object):
    def __init__(self, uid):
        self.__uid = uid
        self.__ball_dict = dict()
        self.__hide_ball_ids = list()

        self.initBall()

    def initBall(self):
        ball_id = 1
        radius = COMMON_RADIUS * COORDINATE_ENLARGE / RADIUS_ENLARGE
        y = random.randint(-radius, radius)
        max_z = int(math.sqrt(pow(radius,2) - pow(y,2)))
        z = random.randint(-max_z, max_z)
        x = random.choice((-1, 1)) * int(math.sqrt(pow(radius,2) - pow(y,2) - pow(z,2)))
        self.__ball_dict[ball_id] = {'ball_id': ball_id, 'ball_x': x, \
                'ball_y': y, 'ball_z': z, 'ball_r': USERBALL_RADIUS}
        # other 7 balls data
        for _bid in xrange(2, 9):
            self.__ball_dict[_bid] = {'ball_id': _bid, 'ball_x': 0, \
                'ball_y': 0, 'ball_z': 0, 'ball_r': 0}
            self.__hide_ball_ids.append(_bid)

        return [(self.__uid, ball_id, x, y, z, USERBALL_RADIUS)]

    def getAllBall(self):
        _all_ball = list()
        for _ball in self.__ball_dict.itervalues():
            if _ball['ball_id'] in self.__hide_ball_ids:
                continue
            _all_ball.append((self.__uid, 
                              _ball['ball_id'],  
                              _ball['ball_x'], 
                              _ball['ball_y'], 
                              _ball['ball_z'],
                              _ball['ball_r']))
        return _all_ball


class PVPRoom(object):
    def __init__(self, room_id):
        self.__id = room_id
        self.__users = dict() # uid:userball
        self.__foodball = dict()
        self.__spineball = dict()
        # hide ball
        self.__hide_foodball_ids = list()
        self.__hide_spineball_ids = list()

    @property
    def count(self):
        return len(self.__users)

    @property
    def room_id(self):
        return self.__id

    def newUser(self, uid):
        if not self.__users:
            # common foodball and spineball
            foodball_conf = get_all_foodball()
            spineball_conf = get_all_spineball()
            self.__foodball = foodball_conf.values()[:500]
            self.__spineball = spineball_conf.values()

        userball_obj = Userball(uid)
        self.__users[uid] = userball_obj
        all_userball = userball_obj.initBall()
        for _ub in self.__users.itervalues():
            all_userball.extend(_ub.getAllBall())

        return (all_userball, self.__foodball, self.__spineball)

    def isMember(self, uid):
        return uid in self.__users

    def syncUserball(self, uid, ball_info):
        if uid not in self.__users:
            return PVPROOM_LOSE, None
                
        pass

