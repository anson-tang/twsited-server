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
from system import *
from constant import *
from errorno import *



@route()
def joinPVP(p, req):
    result = dict()
    foodball_data = get_all_foodball()
    result['foodball'] = foodball_data[:500]
    result['spineball'] = get_all_spineball()

    radius = COMMON_RADIUS * COORDINATE_ENLARGE / RADIUS_ENLARGE
    x = random.randint(-radius, radius)
    y = random.choice((-1, 1)) * int(math.sqrt(radius**2 - x**2))
    z = random.choice((-1, 1)) * int(math.sqrt(radius**2 - x**2 - y**2))

    ballid = 1
    #x = x * 1.0 / radius if x else 0
    #y = y * 1.0 / radius if y else 0
    #z = z * 1.0 / radius if z else 0
    #TODO 数据存内存 包括ballid
    result['userball'] = (ballid, x,y,z)

    return NO_ERROR, result
