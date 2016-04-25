#-*-coding: utf-8-*-
# Version: 0.1
# Author: Don Li <donne.cn@gmail.com>
# License: Copyright(c) 2012 Don.Li
# Summary: 

MAX_SYNC_CNT_PER_LOOP = 1000
SYNC_DB_INTERVAL      = 2 # 2s
KEEP_LIVE_CONNECT = 300 # 5min

ALLOW_NET_DELAY_SECONDS = 5 # 可接受的网络延迟秒数 5s

CS_USER_TOTSEC   = 600
GS_USER_TOTSEC   = 550
GATE_USER_TOTSEC = 400

MAX_SYNC_CNT_PER_LOOP = 1000
SYNC_CS_INTERVAL      = 5
SYNC_DB_INTERVAL      = 2
SYNC_ALLIANCE_INTERVAL = 20


MAX_SYNC_CS_CNT_PER_LOOP = 100

SESSIONKEY_TIMEOUT = 30
SESSION_LOGOUT_REAL = 300  # client logout timeout 5min


GAME_REGION_SEQ = 0 
GAME_REGION_NAME = ''

FOR_ALL         = 0
FOR_SERVER_ONLY = 1
FOR_CLIENT_ONLY = 2

# 不同类型球的半径大小基准值为100倍 取两位有效数字 与客户端相同
FOODBALL_RADIUS = 50
SPINEBALL_RADIUS = 500
USERBALL_RADIUS = 100

COMMON_RADIUS = 10000 # 公共球半径
COORDINATE_ENLARGE = 100 # 公共球半径/坐标 放大的倍数
#COMMON_HIGHT = 10 # 默认高度，高度小于COMMON_RADIUS 表示为去掉顶部和底部某些区域的点.

MAX_ROOM_COUNT = 40 # 房间最大玩家人数


MULTIPLE_HIDE_USERBALL = 1.1 # 玩家球之间互吃的倍数 正常值
MULTIPLE_ENLARGE_FOODBALL = 2 # 吃食物球的半径增长倍数 百分比
MULTIPLE_ENLARGE_USERBALL = 50 # 吃玩家球的半径增长倍数  百分比
INTERVAL_FOODBALL = 20 # 食物球重新随机位置的间隔时间 秒
PVP_SECONDS = 60 # PVP持续时间 秒

