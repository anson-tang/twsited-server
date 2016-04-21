#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 

from systemdata import load_all_config
from log import log
from constant import *

try:
    sysconfig
except NameError:
    sysconfig = load_all_config(FOR_SERVER_ONLY)


def get_all_foodball():
    return sysconfig.get('foodball', list())

def get_all_spineball():
    return sysconfig.get('spineball', list())
