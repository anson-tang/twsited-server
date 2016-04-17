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
