#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 
import logbook 
from tornado import gen
from time import time
from errorno import *
from constant import *
from syslogger import syslogger
from syslogger_constant import *
from attribute import Attribute
from manager.burg import BurgModule
from manager.effect_mgr import EffectMgr
from manager.science_mgr import ScienceMgr
from manager.ranklist_mgr import RanklistMgr
from manager.item_mgr import ItemMgr
from manager.quest_mgr import QuestMgr
from manager.mail_mgr import MailMgr


LOG = logbook.Logger("***Character***")



class Character(object):
    # 玩家下线时需要删除的对象list
    _del_attr = ['burg', 'science_mgr', 'effect_mgr', 'item_mgr', 'quest_mgr', 'mail_mgr']
    def __init__(self, uid, openid, nickname):
        self.uid = uid
        self.openid = openid
        self.nickname = nickname
        self._table = 'character'
        self._where = {'id': uid}
        self._multirow = False
        self.attrib = None
        self._loading = False
        self._futures = list()

        self.burg = BurgModule(self, 'burg')
        self.science_mgr = ScienceMgr(self, 'science')
        self.effect_mgr = EffectMgr(self, 'effect')
        self.item_mgr = ItemMgr(self, 'item')
        self.quest_mgr = QuestMgr(self, 'quest')
        self.mail_mgr = MailMgr(self, 'mail')

        self.all_burgs = None

    @property
    def gem(self):
        return self.attrib.gem
 
    @property
    def item_capacity(self):
        return self.attrib.item_capacity

    @property
    def vip_seconds(self):
        now = int(time())
        return max((self.attrib.vip_end_time or 0) - now, 0)
 
    def get_attr(self, name):
        if hasattr(self.attrib, name):
            return getattr(self.attrib, name)
        return 0

    @gen.coroutine
    def baseinfo(self):
        now = int(time())
        # 更新城池资源
        self.burg.calculate_resource(now)

        _values = self.attrib.value
        _values['vip_seconds'] = max((self.attrib.vip_end_time or 0) - now, 0)
        _values.update(self.burg.value)
        _values['equips'] = yield self.item_mgr.equip_info(self.burg.burg_id)
        raise gen.Return(_values)

    @gen.coroutine
    def load(self):
        if not self.attrib:
            if self._loading is False:
                self._loading = True
                self.attrib = yield Attribute.load(self._table, self._where, self._multirow)
                # 同时加载effect
                yield self.effect_mgr.load()
                # 加载burg信息
                yield self.burg.info()
                # 更新ongoing数据
                self.burg.update()

                for _f in self._futures:
                    _f.set_result(True)

                self._loading = False
                self._futures = list()
            else:
                _f = Future()
                self._futures.append(_f)
                yield _f
 
    @gen.coroutine
    def new(self, nickname):
        self.attrib = Attribute(self._table)
        yield self.attrib.new(id=self.uid, openid=self.openid, nickname=nickname, gem=100000, \
            golds=100000, burg_num=1, item_capacity=MAX_ITEM_CAPACITY, quest_over=0)
        self.nickname = nickname
        # create burg
        yield self.burg.create_burg(self.attrib.burg_num)

        # create effect table
        yield self.effect_mgr.new(food_percent=0, wood_percent=0, stone_percent=0, \
            steel_percent=0, protect_percent=0, attack_percent=0, hp_percent=0, destroy_self_odds=0, \
            destroy_other_odds=0, carry_percent=0, rate_percent=0)
        # create first quest
        yield self.quest_mgr.init_quest()
        syslogger(LOG_CHAR_NEW, self.uid, nickname)

    def logout(self):
        LOG.info("user(%s) logout." % self.uid)
        syslogger(LOG_LOGOUT, self.uid)
        for _mgr in Character._del_attr:
            if hasattr(self, _mgr) and _mgr in self.__dict__:
                del self.__dict__[_mgr]

    @gen.coroutine
    def load_all_burgs(self):
        if self.all_burgs is not None:
            return

        _burgs = {self.burg.burg_id: self.burg}
        for _idx in xrange(1, self.attrib.burg_num+1):
            if _idx == self.burg.burg_id:
                continue
            burg = BurgModule(self, 'burg')
            yield burg.load(burg_id=_idx)
            _burgs[_idx] = burg

        self.all_burgs = _burgs 

    @gen.coroutine
    def get_all_burgs(self):
        yield self.load_all_burgs()

        raise gen.Return(self.all_burgs)

    def get_attack_percent(self, soldier_type, had_hero=False):
        '''
        @summary: 计算科技 英雄 装备 加成效果
        @param: had_hero-英雄状态 True:参战
        '''
        percent = self.item_mgr.get_equip_attack(soldier_type)
        LOG.debug('========= attack uid:%s, equip percent:%s.'%(self.uid, percent))
        percent += self.effect_mgr.get_attr('attack_percent')
        LOG.debug('========= attack uid:%s, science percent:%s.'%(self.uid, percent))
        if had_hero and soldier_type == SOLDIER_TYPE_CAVALRY:
            percent += self.burg.get_attr('attack_percent')
            LOG.debug('========= attack uid:%s, hero percent:%s.'%(self.uid, percent))

        return percent

    def get_defence_percent(self, soldier_type, had_hero=False):
        '''
        @summary: 计算科技 英雄 装备 加成效果
        '''
        percent = self.item_mgr.get_equip_defence(soldier_type)
        LOG.debug('========= defence uid:%s, equip percent:%s.'%(self.uid, percent))
        percent += self.effect_mgr.get_attr('hp_percent')
        LOG.debug('========= defence uid:%s, science percent:%s.'%(self.uid, percent))
        if had_hero and soldier_type == SOLDIER_TYPE_CAVALRY:
            percent += self.burg.get_attr('hp_percent')
            LOG.debug('========= defence uid:%s, hero percent:%s.'%(self.uid, percent))

        return percent

    def add_gem(self, num):
        self.attrib.gem += abs(num)

    def use_gem(self, num):
        '''
        @summary: 使用充值币
        '''
        if num <= 0:
            return REQUEST_FAILURE_ERROR
        if num > self.attrib.gem:
            return GEM_NOT_ENOUGH_ERROR
        self.attrib.gem -= num
        return NO_ERROR

    def add_golds(self, golds):
        self.attrib.golds += abs(golds)

    def sub_golds(self, golds):
        self.attrib.golds -= abs(golds)

    def update_quest_over(self):
        self.attrib.quest_over = 1

    def update_vip_end_time(self, seconds):
        '''
        @summary: 更新vip截止时间 初值和玩家创建时间相同
        '''
        if not self.attrib.vip_end_time or \
                self.attrib.vip_end_time == self.attrib.create_time:
            self.attrib.vip_end_time = int(time()) + abs(seconds)
        else:
            self.attrib.vip_end_time += abs(seconds)

