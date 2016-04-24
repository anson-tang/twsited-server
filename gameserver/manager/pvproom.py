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
from errorno import *

class Userball(object):
    def __init__(self, uid):
        self.__uid = uid
        self.__ball_dict = dict()
        self.__hide_ball_ids = list()

        self.initBall()

    @property
    def uid(self):
        return self.__uid

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
        #log.debug('__ball_dict:{0}'.format(self.__ball_dict))
        _all_ball = list()
        for _bid, _ball in self.__ball_dict.iteritems():
            if _ball['ball_id'] in self.__hide_ball_ids:
                self.__ball_dict[_bid] = {'ball_id': _bid, 'ball_x': 0, \
                    'ball_y': 0, 'ball_z': 0, 'ball_r': 0}
                continue
            _all_ball.append((self.__uid, 
                              _ball['ball_id'],  
                              _ball['ball_x'], 
                              _ball['ball_y'], 
                              _ball['ball_z'],
                              _ball['ball_r']))
        return _all_ball

    def hideBall(self, ball_id):
        if ball_id not in self.__hide_ball_ids:
            self.__hide_ball_ids.append(ball_id)


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
            self.__foodball = get_all_foodball()
            self.__spineball = get_all_spineball()
            foodball_conf = self.__foodball.values()[:500]
            spineball_conf = self.__spineball.values()
        else:
            foodball_conf = self.__foodball.values()[:500]
            spineball_conf = self.__spineball.values()

        userball_obj = Userball(uid)
        self.__users[uid] = userball_obj
        all_userball = userball_obj.initBall()
        for _ub in self.__users.itervalues():
            if _ub.uid == uid:
                continue
            all_userball.extend(_ub.getAllBall())

        return (all_userball, foodball_conf, spineball_conf)

    def isMember(self, uid):
        return uid in self.__users

    def syncUserball(self, uid, ball_info):
        if uid not in self.__users:
            return PVPROOM_LOSE, None
        _hide_fbids = list()
        _hide_ubids = list()
        # first, check eat self
        for ball_id, ball_x, ball_y, ball_z, ball_r in ball_info:
            #TODO 和食物球 其它玩家球比较半径大小 计算直线距离
            #TODO 玩家球 分裂后的半径也会比食物球大吗？
            pow_r = pow(ball_r, 2)
            for _bid, _bx, _by, _bz in self.__foodball.itervalues():
                _distance = pow(ball_x-_bx, 2) + pow(ball_y-_by, 2) + pow(ball_z-_bz, 2)
                if _distance < pow_r:
                    self.__hide_foodball_ids.append(_bid)
                    _hide_fbids.append(_bid)
            for _bid in _hide_fbids:
                del self.__foodball[_bid]
            # uid and ballid
            for _ub in self.__users.itervalues():
                _all_ball = _ub.getAllBall()
                for _uid, _bid, _bx, _by, _bz, _br in _all_ball:
                    if _br > ball_r:
                        continue
                    _distance = pow(ball_x-_bx, 2) + pow(ball_y-_by, 2) + pow(ball_z-_bz, 2)
                    if _distance < pow_r:
                        _ub.hideBall(_bid)
                        _hide_ubids.append((uid, _bid))

        #TODO 食物球被吃后的出现规则
        #TODO broadcast

        data = (_hide_ubids, _hide_fbids) if (_hide_ubids or _hide_fbids) else list()
        return NO_ERROR, data
