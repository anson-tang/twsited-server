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

MAX_BROADCAST_PER_LOOP = 100

# 不同类型球的半径大小基准值为100倍 取两位有效数字 与客户端相同
FOODBALL_RADIUS = 50
SPINEBALL_RADIUS = 500
USERBALL_RADIUS = 100

COMMON_RADIUS = 10000 # 公共球半径
COORDINATE_ENLARGE = 100 # 公共球半径/坐标 放大的倍数

MAX_COMMON_RADIUS = 5000 # 公共球最大半径
MAX_USER_COUNT = 20 # 房间最大玩家人数
MAX_USERBALL_COUNT = 8 # 玩家球最大数量

INIT_USERBALL_VOLUME = 8 # 玩家球初始体积
INIT_FOODBALL_VOLUME = 4 # 食物球初始体积
INIT_SPINEBALL_VOLUME = 40 # 刺球初始体积


MULTIPLE_HIDE_USERBALL = 1.1 # 玩家球之间互吃的倍数 正常值
MULTIPLE_ENLARGE_FOODBALL = 2 # 吃食物球的半径增长倍数 百分比
MULTIPLE_ENLARGE_USERBALL = 50 # 吃玩家球的半径增长倍数  百分比
REFRESH_INTERVAL_FOODBALL = 15 # 食物球重新随机位置的间隔时间 秒
REFRESH_INTERVAL_SPINEBALL = 30 # 刺球刷新间隔时间 秒
PVP_SECONDS = 300 # PVP持续时间 秒

