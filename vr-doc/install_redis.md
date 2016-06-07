0)  $ sudo apt-get install -y make gcc python-dev
1)  $ wget http://download.redis.io/releases/redis-3.0.7.tar.gz
2)  $ tar xzf redis-3.0.7.tar.gz
3)  $ cd redis-3.0.7/deps
4)  $ make hiredis lua jemalloc linenoise
5)  $ cd redis-3.0.7
6)  $ make 
7)  $ make install
8)  $ cd redis-3.0.7/utils
9)  $ ./install_server.sh
10) $ service redis_6379 status

-------------------------------
$ vim /etc/redis/6379.conf
bind 127.0.0.1
requirepass <Redis.Passwd>
port 10379
rename-command CONFIG ""
#run not root
redis-server -c /etc/redis/6379.conf

# client登录
$ redis-cli -p 10379 -a Redis.Passwd
