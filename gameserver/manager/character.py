#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 

from twisted.internet import defer
from time import time
from log import log
from errorno import *
from constant import *
from attribute import Attribute



class Character(object):
    # 玩家下线时需要删除的对象list
    _del_attr = []
    def __init__(self, uid=None, machine_code=None, nickname=None):
        self.uid = uid if uid else 0
        self.machine_code = machine_code if machine_code else ''
        self.nickname = nickname if nickname else ''
        self._table = 'character'
        self._where = {'machine_code': machine_code}
        self._multirow = False
        self.attrib = None
        self._loading = False
        self._futures = list()

    @property
    def coin(self):
        return self.attrib.coin
 
    def get_attr(self, name):
        if hasattr(self.attrib, name):
            return getattr(self.attrib, name)
        return 0

    def info(self):
        log.debug("value:{0}".format(self.attrib.value))
        return self.attrib.value

    @defer.inlineCallbacks
    def load(self):
        if not self.attrib:
            if self._loading is False:
                self._loading = True
                self.attrib = yield Attribute.load(self._table, self._where, self._multirow)
                # no other data to load

                for _f in self._futures:
                    _f.set_result(True)

                self._loading = False
                self._futures = list()
            else:
                _f = Future()
                self._futures.append(_f)
                yield _f
 
    @defer.inlineCallbacks
    def new(self, machine_code, nickname):
        self.attrib = Attribute(self._table)
        yield self.attrib.new(machine_code=machine_code, nickname=nickname, max_weight=0, \
                play_num=0, eat_num=0, be_eated_num=0)
        self.uid = self.attrib.attrib_id
        self.nickname = nickname
        self.machine_code = machine_code

    def logout(self):
        LOG.info("user(%s) logout." % self.uid)
        for _mgr in Character._del_attr:
            if hasattr(self, _mgr) and _mgr in self.__dict__:
                del self.__dict__[_mgr]

    def add_coin(self, coin):
        self.attrib.coin += abs(coin)

    def use_coin(self, coin):
        self.attrib.coin -= abs(coin)

