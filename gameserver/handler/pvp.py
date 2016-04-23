#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 
import random
import math

from rpc import route
from log import log
from constant import *
from errorno import *
from manager.pvpserver import g_PVPServer



@route()
def joinPVP(p, req):
    if hasattr(p, "uid"):
        log.debug('uid:{0}'.format(p.uid))
        uid = p.uid
    else: # used to test
        uid = 1
    _u, _f, _s = g_PVPServer.joinRoom(uid)

    result = dict(userball=_u, foodball=_f, spineball=_s)

    return NO_ERROR, result
