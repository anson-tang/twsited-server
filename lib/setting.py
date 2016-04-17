#-*-coding: utf-8-*-

#关闭后，一些debug功能会被关闭，不影响log等级
DEBUG = True                                 

#可设置为: 'debug', 'info', 'warn', 'error', 'crit'
LOG_THRESHOLD = 'debug'                      

#服务器运行日志的绝对路径
LOG_PATH = '/home/likai/3d3k/Program/trunk/Server/logs/' 

#日志文件多大时会被rotate
LOG_ROTATE_INTERVAL = 104857600              

#最多接受客户端TCP连接数
MAX_CLIENTS_PER_SVC = 5000                   


#游戏区DB配置
DB_CONF = {
        'host'         : '127.0.0.1',        #MySQL服务器TCP地址, 最好使用局域网地址，不要开放到外网
        'port'         : 3306,               #MySQL服务器TCP端口
        'user'         : 'vrgame',           #MySQL账号
        'pass'         : 'db1234',           #账号的密码
        'userdb'       : 'vr_userdb',        #玩家数据database名称
        'pool_size'    : 50                  #持久连接池最大同时连接数
    }

#游戏区Redis配置
REDIS_CONF = {
        'redis_sock'   : '/tmp/redis.sock',  #Redis服务器Unix Socket地址。如果没有启用，请置空。
        'redis_host'   : '127.0.0.1',        #当redis_sock为空时，Redis服务器TCP地址, 最好使用局域网，不要开放到外网
        'redis_port'   : 6379,               #当redis_sock为空时，Redis服务器TCP端口
        'redis_db'     : 2,                   #本服使用的Redis服务器db序号
        'redis_passwd' : 'Redis.Passwd',
    }

SERVER_ID = 101
HOST_GAME = '127.0.0.1'
PORT      = 12000
execfile(__file__.rsplit('/', 1)[0] + '/../etc/setting_env.py')

#游戏区游戏服务器配置
GAMESERVER = {
        'server_id' : SERVER_ID + 10,     #游戏服务器编号
        'hostname'  : HOST_GAME,          #游戏服务器IP地址
        'port'      : PORT + 10,          #游戏服务器TCP端口
        'adminport' : PORT + 11           #游戏服务器ADMIN端口，只会在localhost接口上监听
    }

