# twsited-server

# ubuntu 
$ apt-get install -y python-pip python-dev

# first need to install base package
$ cd twsited-server

$ pip install -r requirement.txt

# install mysql and create database, init database
do it as 

https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-14-04

http://www.devopsservice.com/installation-of-mysql-server-5-7-on-ubuntu-14-04/

---------------------------------
## Question
ImportError: No module named MySQLdb

$ apt-get install python-mysqldb

----------------------------------
## install package
1) shell> wget http://dev.mysql.com/get/mysql-apt-config_0.6.0-1_all.deb

2) shell> dpkg -i mysql-apt-config_0.6.0-1_all.deb

3) shell> apt-get update

4) shell> apt-get install mysql-server

5) shell> mysql_secure_installation

6) shell> mysql_install_db

7) shell> service mysql status

8) shell> mysqladmin -p -u root version


---------------------------------
## create database
$ mysql -uroot -p

1) mysql> create database vr_userdb character set utf8 collate utf8_bin;

Query OK, 1 row affected (0.00 sec)

2) mysql> create user 'vr'@'127.0.0.1' identified by 'Vr-0#Ser.ver';

Query OK, 0 rows affected (0.00 sec)

3) mysql> grant all privileges on vr_userdb.* to 'vr'@'127.0.0.1' identified by 'Vr-0#Ser.ver';

Query OK, 0 rows affected, 1 warning (0.00 sec)

4) mysql> flush privileges;

Query OK, 0 rows affected (0.00 sec)

5) 

1) mysql> create database vr_sysconfigdb character set utf8 collate utf8_bin;

Query OK, 1 row affected (0.00 sec)

2) mysql> grant all privileges on vr_sysconfigdb.* to 'vr'@'127.0.0.1' identified by 'Vr-0#Ser.ver';

Query OK, 0 rows affected, 1 warning (0.00 sec)

3) mysql> flush privileges;

Query OK, 0 rows affected (0.00 sec)


---------------------------------
## init database
$ mysql -uvr -p vr_userdb < twisted-server/sql/userdb.sql

$ mysql -uvr -p vr_sysconfigdb < twisted-server/sql/sysconfigdb.sql


# install redis and update conf file
## install redis
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
## update conf file and start server
$ vim /etc/redis/6379.conf

bind 127.0.0.1

requirepass <Redis.Passwd>

port 10379

rename-command CONFIG ""

// run not root

redis-server -c /etc/redis/6379.conf

// client登录

$ redis-cli -p 10379 -a Redis.Passwd


# update setting_env.py
$ cd twsited-server

$ cp etc/setting_env_eg.py etc/setting_env.py

$ vim etc/setting_env.py

// 更新DB_CONF REDIS_CONF HOST_GAME PORT为实际参数




# start/stop/restart twisted-server
$ cd twsited-server

$ ./start.sh

$ ./stop_real.sh

$ ./restart.sh


