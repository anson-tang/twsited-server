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
from handler.broadcast import send2client




class Userball(object):
    def __init__(self, uid):
        self.__uid = uid
        self.__ball_dict = dict() # {bid: [uid,bid,bx,by,bz,br], ...}
        self.__hide_ball_ids = list()

        self.initBall()

    @property
    def uid(self):
        return self.__uid

    def initBall(self):
        ball_id = 1
        radius = COMMON_RADIUS
        y = random.randint(-radius, radius)
        max_z = int(math.sqrt(pow(radius,2) - pow(y,2)))
        z = random.randint(-max_z, max_z)
        x = random.choice((-1, 1)) * int(math.sqrt(pow(radius,2) - pow(y,2) - pow(z,2)))
        self.__ball_dict[ball_id] = [self.__uid, ball_id, x, y, z, USERBALL_RADIUS]

        return self.__ball_dict.values()

    def getAllBall(self):
        _all_ball = list()
        for _bid, _ball in self.__ball_dict.iteritems():
            if _bid in self.__hide_ball_ids:
                continue
            _all_ball.append(_ball)
        return _all_ball

    def getHideBall(self, ball_id):
        if ball_id not in self.__hide_ball_ids:
            self.__hide_ball_ids.append(ball_id)

    def setHideBall(self, ball_id):
        if ball_id in self.__ball_dict:
            del self.__ball_dict[ball_id]

    def checkHideBall(self, ball_info=None):
        ''' check eat self '''
        if not ball_info:
            return list()
        log.debug('=====test start ===== ball_info:{0}'.format(ball_info))
        ball_info = sorted(ball_info, key=lambda ball_info: ball_info[4], reverse=True)
        for _b in ball_info:
            _b.append(pow(_b[4]*COORDINATE_ENLARGE, 2))
        total = len(ball_info)
        loop = 1
        hide_ids = list()
        delta_radius = dict()
        new_ball_info = ball_info[:1]
        while loop < total:
            ball_id, ball_x, ball_y, ball_z, ball_r, pow_r = ball_info[loop-1]
            if ball_id in hide_ids:
                loop = loop + 1
                continue
            for _bid, _bx, _by, _bz, _br, _pr in ball_info[loop:]:
                if _bid in hide_ids or not (_bx or _by or _bz):
                    continue
                if ball_r < MULTIPLE_HIDE_USERBALL*_br:
                    new_ball_info.append((_bid, _bx, _by, _bz, _br, _pr))
                    continue
                _distance = pow(ball_x-_bx, 2) + pow(ball_y-_by, 2) + pow(ball_z-_bz, 2)
                if _distance < pow_r:
                    hide_ids.append(_bid)
                    delta_radius[ball_id] = new_ball_r.setdefault(ball_id, ball_r) + (MULTIPLE_ENLARGE_USERBAL * _br / 100)
                else:
                    new_ball_info.append((_bid, _bx, _by, _bz, _br, _pr))
            loop = loop + 1

        hide_ids = [(self.__uid, _bid) for _bid in hide_ids]
        log.debug('=====test final ===== hide_ids:{0}, delta_radius:{1}, new_ball_info:{2}'.format(hide_ids, new_ball_r, new_ball_info))
        return hide_ids, delta_radius, new_ball_info


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
            foodball_conf = self.__foodball.values()
            spineball_conf = self.__spineball.values()
        else:
            foodball_conf = self.__foodball.values()
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
        if not (ball_info and isinstance(ball_info[0], list)):
            log.error("args error. uid:{0}, ball_info:{1}.".format(uid, ball_info))
            return ARGS_ERROR, None

        if uid not in self.__users:
            return PVPROOM_LOSE, None

        _hide_fb_ids = list()

        userball_obj = self.__users[uid]
        _hide_ub_ids, delta_radius, ball_info = userball_obj.checkHideBall(ball_info)

        for _bid, _bx, _by, _bz in self.__foodball.itervalues():
            _distance = pow(ball_x-_bx, 2) + pow(ball_y-_by, 2) + pow(ball_z-_bz, 2)
            for ball_id, ball_x, ball_y, ball_z, ball_r, pow_r in ball_info:
                #TODO 和食物球 其它玩家球比较半径大小 计算直线距离
                #TODO 玩家球 分裂后的半径也会比食物球大吗？
                log.warn('uid:{0}, pow_r:{1}, _distance:{2}, source:{3}, target:{4}.'.format(uid, pow_r, _distance, (ball_id, ball_x, ball_y, ball_z, ball_r), (_bid, _bx, _by, _bz)))
                if _distance < pow_r:
                    #TODO 自身体积增长
                    _delta_br = ball_r * MULTIPLE_ENLARGE_FOODBALL / 100
                    _new_ub_info[_bid] = _new_ub_info.setdefault(_bid, ball_r) + _delta_br
                    self.__hide_foodball_ids.append(_bid)
                    _hide_fb_ids.append(_bid)
            for _bid in _hide_fb_ids:
                del self.__foodball[_bid]
        # uid and ballid
        for _ub in self.__users.itervalues():
            if _ub.uid == uid:
                continue
            _all_ball = _ub.getAllBall()
            for _uid, _bid, _bx, _by, _bz, _br in iter(_all_ball):
                for ball_id, ball_x, ball_y, ball_z, ball_r, pow_r in ball_info:
                    if MULTIPLE_HIDE_USERBALL*_br > ball_r:
                        continue
                    _distance = pow(ball_x-_bx, 2) + pow(ball_y-_by, 2) + pow(ball_z-_bz, 2)
                    if _distance < pow_r:
                        #TODO 自身体积增长
                        delta_radius[ball_id] = delta_radius.setdefault(ball_id, ball_r) + (MULTIPLE_ENLARGE_USERBAL * _br / 100)
                        _ub.setHideBall(_bid)
                        _hide_ub_ids.append((uid, _bid))

        #TODO 食物球被吃后的出现规则
        data = list()
        _delta_ub_radius = [(_k, _v) for _k, _v in delta_radius.iteritems()]
        if (_hide_ub_ids or _hide_fb_ids or _delta_ub_radius):
            data = (_hide_ub_ids, _hide_fb_ids, _delta_ub_radius)
            #TODO broadcast
            uids = self.__users.keys()
            log.debug('================broadcast uid:{0}, users: {1}).'.format(uid, uids))
            uids.remove(uid)
            if uids:
                send2client(uids, 'broadcastUserball', data)

        log.warn('uid:{0}, data:{1}'.format(uid, data))
        return NO_ERROR, data
