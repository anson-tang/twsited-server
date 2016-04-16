#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Don Li <donne.cn@gmail.com>
# License: Copyright(c) 2013 Don.Li
# Summary: 

import setting
from dbhelper import DBHelper

try:
    POOL
except NameError:
    POOL = DBHelper(**setting.DB_CONF)
