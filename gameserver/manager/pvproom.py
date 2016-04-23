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

        self.initBall()

    def initBall(self):
        ball_id = 1
        radius = COMMON_RADIUS * COORDINATE_ENLARGE / RADIUS_ENLARGE
        y = random.randint(-radius, radius)
        max_z = int(math.sqrt(radius**2 - y**2))
        z = random.randint(-max_z, max_z)
        x = random.choice((-1, 1)) * int(math.sqrt(radius**2 - y**2 - z**2))
        self.__ball_dict[ball_id] = dict(ball_id=ball_id, ball_x=x, ball_y=y, ball_z=z, is_show=True)
        # other 7 balls data
        for _id in xrange(2, 9):
            self.__ball_dict[_id] = dict(ball_id=_id, ball_x=0, ball_y=0, ball_z=0, is_show=False)

        return ((ball_id, x, y, z),)


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
        userball = userball_obj.initBall()
        return (userball, self.__foodball, self.__spineball)

    def syncUserball(self):
        pass

