#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 
import random
import math

from time import time
from twisted.internet import defer, reactor
from log import log
from system import *
from constant import *
from errorno import *
from redis_constant import *
from redis import redis
from handler.broadcast import send2client
from manager.gameuser import g_UserMgr


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
        self.__ball_dict[ball_id] = [self.__uid, ball_id, x, y, z, USERBALL_RADIUS, INIT_USERBALL_VOLUME, 0]

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

    def updateVolume(self, delta_volume):
        for _bid, _volume in delta_volume.iteritems():
            self.__ball_dict[_bid][6] = _volume

    def checkHideBall(self, base_ball=None):
        ''' check eat self '''
        if not base_ball:
            return list()
        base_ball = sorted(base_ball, key=lambda base_ball: base_ball[6], reverse=True)
        self.__ball_dict = dict()
        ball_info = list()
        for _b in base_ball:
            if _b[0] != self.__uid:
                log.error('invalid userball data. uid:{0}, ball:{1}'.format(self.__uid, _b))
                continue
            self.__ball_dict[_b[1]] = [_b[0], _b[1], _b[2], _b[3], _b[4], _b[5], _b[6], _b[7]]
            _b.append(pow(_b[5], 2))
            ball_info.append(_b)

        total = len(ball_info)
        loop = 1
        hide_ids = list()
        delta_volume = dict()
        new_ball_info = ball_info[:1]
        while loop < total:
            uid, ball_id, ball_x, ball_y, ball_z, ball_r, ball_v, ball_s, pow_r = ball_info[loop-1]
            if ball_id in hide_ids:
                loop = loop + 1
                continue
            for _uid, _bid, _bx, _by, _bz, _br, _bv, _bs, _pr in ball_info[loop:]:
                if _bid in hide_ids or not (_bx or _by or _bz):
                    continue
                if ball_v < MULTIPLE_HIDE_USERBALL*_bv:
                    new_ball_info.append((_uid, _bid, _bx, _by, _bz, _br, _bv, _bs, _pr))
                    continue
                _distance = pow(ball_x-_bx, 2) + pow(ball_y-_by, 2) + pow(ball_z-_bz, 2)
                if _distance < pow_r:
                    hide_ids.append(_bid)
                    del self.__ball_dict[_bid]
                    delta_volume[ball_id] = delta_volume.setdefault(ball_id, ball_v) + _bv
                else:
                    new_ball_info.append((_uid, _bid, _bx, _by, _bz, _br, _bv, _bs, _pr))
            loop = loop + 1

        new_ball_info = [ _b for _b in ball_info if _b[1] not in hide_ids]
        hide_ids = [(self.__uid, _bid) for _bid in hide_ids]
        return hide_ids, delta_volume, new_ball_info


class PVPRoom(object):
    def __init__(self, room_id):
        self.__id = room_id
        self.__users = dict() # uid:userball
        self.__foodball = dict()
        self.__spineball = dict()
        # hide ball
        self.__hide_foodball_ids = dict()
        self.__hide_spineball_ids = list()
        # PVP结束时间点
        self.__end_time = 0
        self.__end_tag = False
        # 统计吞噬和被吞噬次数
        self.__eat_num = dict()  # uid-num
        self.__be_eated_num = dict() # uid-num

        self.__call_id = reactor.callLater(REFRESH_INTERVAL_FOODBALL, self._broadcastFoodball)


    @property
    def count(self):
        return len(self.__users)

    @property
    def room_id(self):
        return self.__id

    @property
    def isEnd(self):
        if self.__end_tag:
            return True

        _now_time = int(time()*1000)
        if not self.__end_time or _now_time < self.__end_time:
            return False
        else:
            if self.__call_id.active():
                self.__call_id.cancel()
            self.__end_tag = True
            return True

    def isMember(self, uid):
        return uid in self.__users

    @defer.inlineCallbacks
    def newUser(self, uid):
        if not self.__users:
            # common foodball and spineball
            self.__foodball = get_all_foodball()
            self.__spineball = get_all_spineball()
            foodball_conf = self.__foodball.values()
            spineball_conf = self.__spineball.values()
            self.__end_time = int((time() + PVP_SECONDS)*1000)
            self.__eat_num.setdefault(uid, 0)
            self.__be_eated_num.setdefault(uid, 0)
            reactor.callLater(PVP_SECONDS, self._broadcastFoodball)
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
        yield redis.zadd(SET_RANK_ROOM_VOLUME%self.__id, uid, -INIT_USERBALL_VOLUME)
        rank = yield redis.zrank(SET_RANK_ROOM_VOLUME%self.__id, uid)
        rank = 0 if rank is None else int(rank) + 1

        data = {'userball': all_userball, \
                'foodball': foodball_conf, \
                'spineball': spineball_conf, \
                'end_time': self.__end_time, \
                'total': self.count, 
                'rank': rank, \
                'room_id': self.__id,
                }
        defer.returnValue(data)

    @defer.inlineCallbacks
    def syncUserball(self, character, ball_info):
        if not (ball_info and isinstance(ball_info[0], list)):
            log.error("args error. uid:{0}, ball_info:{1}.".format(uid, ball_info))
            defer.returnValue((ARGS_ERROR, None))

        uid = character.attrib_id
        if uid not in self.__users:
            defer.returnValue((PVPROOM_LOSE, None))

        _hide_fb_ids = list()
        userball_obj = self.__users[uid]
        _hide_ub_ids, _delta_volume, ball_info = userball_obj.checkHideBall(ball_info)

        #_delta_br =  int(FOODBALL_RADIUS * MULTIPLE_ENLARGE_FOODBALL * 0.01)
        _max_hide = 1
        for _bid, _bx, _by, _bz in self.__foodball.itervalues():
            for _, ball_id, ball_x, ball_y, ball_z, ball_r, ball_v, ball_s, pow_r in ball_info:
                # 和食物球 其它玩家球比较半径大小 计算直线距离
                # 玩家球 分裂后的半径也会比食物球大吗？
                _distance = pow(ball_x-_bx, 2) + pow(ball_y-_by, 2) + pow(ball_z-_bz, 2)
                if _distance < pow_r:
                    log.debug('--------------- eated foodball uid:{0}, pow_r:{1}, _distance:{2}, source:{3}, target:{4}, _delta_volume:{5}.'.format(uid, pow_r, _distance, (ball_id, ball_x, ball_y, ball_z, ball_r), (_bid, _bx, _by, _bz), _delta_volume))
                    # 自身体积增长
                    _delta_volume[ball_id] = _delta_volume.setdefault(ball_id, ball_v) + INIT_FOODBALL_VOLUME
                    _hide_fb_ids.append(_bid)
                if len(_hide_fb_ids) > 2:
                    break
        for _bid in _hide_fb_ids:
            self.__hide_foodball_ids[_bid] = 0
            if _bid in self.__foodball:
                del self.__foodball[_bid]
        # uid and ballid
        for _ub in self.__users.itervalues():
            if _ub.uid == uid:
                continue
            _all_ball = _ub.getAllBall()
            for _uid, _bid, _bx, _by, _bz, _br, _bv, _bs in iter(_all_ball):
                _be_eated_user = g_UserMgr.getUserByUid(_uid)
                for _, ball_id, ball_x, ball_y, ball_z, ball_r, ball_v, ball_s, pow_r in ball_info:
                    if MULTIPLE_HIDE_USERBALL*_bv > ball_v:
                        continue
                    _distance = pow(ball_x-_bx, 2) + pow(ball_y-_by, 2) + pow(ball_z-_bz, 2)
                    if _distance < pow_r:
                        log.debug('---------------- eated userball uid:{0}, pow_r:{1}, _distance:{2}, source:{3}, target:{4}.'.format(uid, pow_r, _distance, (_uid, _bid, _bx, _by, _bz, _br), (ball_id, ball_x, ball_y, ball_z, ball_r)))
                        # 记录吞噬/被吞噬 玩家球的个数
                        character.eat_num += 1
                        self.__eat_num[uid] += 1
                        if _be_eated_user and _be_eated_user.attrib:
                            _be_eated_user.attrib.be_eated_num += 1
                            self.__be_eated_num[_uid] = self.__be_eated_num.setdefault(_uid, 0) + 1

                        # 自身体积增长
                        _delta_volume[ball_id] = _delta_volume.setdefault(ball_id, ball_v) + _bv
                        _ub.setHideBall(_bid)
                        _hide_ub_ids.append((_uid, _bid))
                        yield redis.zincrby(SET_RANK_ROOM_VOLUME%self.__id, _uid, _bv)

        data = list()
        _delta_ub_data = list()
        _delta_ub_volume = 0
        for _, ball_id, ball_x, ball_y, ball_z, ball_r, ball_v, ball_s, pow_r in ball_info:
            ball_v = _delta_volume[ball_id] if ball_id in _delta_volume else ball_v
            _delta_ub_data.append((uid, ball_id, ball_x, ball_y, ball_z, ball_r, ball_v, ball_s))
            _delta_ub_volume += ball_v
        yield redis.zadd(SET_RANK_ROOM_VOLUME%self.__id, uid, -_delta_ub_volume)
        # 更新自己的球体积信息
        userball_obj.updateVolume(_delta_volume)
        if (_hide_ub_ids or _hide_fb_ids or _delta_ub_data):
            data = [_hide_ub_ids, _hide_fb_ids, _delta_ub_data]
            #TODO broadcast
            uids = self.__users.keys()
            uids.remove(uid)
            if uids:
                send2client(uids, 'broadcastUserball', data)

        _rank = yield redis.zrank(SET_RANK_ROOM_VOLUME%self.__id, uid)
        _rank = 0 if _rank is None else int(_rank) + 1 
        _total = len(self.__users)
        data.append((_rank, _total))
        defer.returnValue((NO_ERROR, data))

    def syncSpineball(self, uid, ball_info):
        if not (ball_info and isinstance(ball_info[0], list)):
            log.error("args error. ball_info:{0}.".format(ball_info))
            return ARGS_ERROR, None

        uids = self.__users.keys()
        uids.remove(uid)
        if uids:
            send2client(uids, 'broadcastSpineball', ball_info)

        return NO_ERROR, None

    @defer.inlineCallbacks
    def overPVP(self):
        ''' 战斗结算 '''
        for _uid in self.__users.iterkeys():
            yield redis.zadd(SET_RANK_ROOM_EAT%self.__id, _uid, -self.__eat_num.get(_uid, 0))
            yield redis.zadd(SET_RANK_ROOM_EATED%self.__id, _uid, -self.__be_eated_num.get(_uid, 0))
            _user_mgr = g_UserMgr.getUserByUid(_uid)
            _user_mgr.attrib.paly_num += 1
            _volume = yield redis.zscore(SET_RANK_ROOM_VOLUME%self.__id, _uid)
            _weight = int(_volume) * 10 if _volume else 0
            if _user_mgr.attrib.max_weight < _weight:
                _user_mgr.attrib.max_weight = _weight
                yield redis.zadd(SET_RANK_PVP_WEIGHT, _uid, -_weight)

        yield redis.hset(HASH_PVP_ROOM_USER_NUM, self.__id, self.count)

    def _broadcastFoodball(self):
        ''' 食物球被吃后的出现规则 '''
        _uids = self.__users.keys()
        _foodball_ids = self.__hide_foodball_ids.keys()
        _new_foodball_info = self._random_xyz(_foodball_ids)
        if _uids and _foodball_ids:
            send2client(_uids, 'broadcastNewFoodball', _new_foodball_info)
        self.__hide_foodball_ids = dict()

        if not self.isEnd:
            if self.__call_id.active():
                self.__call_id.cancel()
            self.__call_id = reactor.callLater(REFRESH_INTERVAL_FOODBALL, self._broadcastFoodball)

    def _random_xyz(self, ball_ids):
        values = list()
        radius = COMMON_RADIUS
        for _id in ball_ids:
            y = random.randint(-radius, radius)
            max_z = int(math.sqrt(pow(radius,2) - pow(y,2)))
            z = random.randint(-max_z, max_z)
            x = random.choice((-1, 1)) * int(math.sqrt(pow(radius,2) - pow(y,2) - pow(z,2)))
            values.append((_id, x, y, z))
            self.__foodball[_id] = (_id, x, y, z)

        return values
