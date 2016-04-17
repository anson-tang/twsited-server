do it as 
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-14-04
http://www.devopsservice.com/installation-of-mysql-server-5-7-on-ubuntu-14-04/

----------------------------------
1) shell> sudo apt-get update
2) shell> sudo apt-get mysql-server
3) shell> wget http://dev.mysql.com/get/mysql-apt-config_0.6.0-1_all.deb
4) shell> dpkg -i mysql-apt-config_0.6.0-1_all.deb
5) shell> apt-get install mysql-server
6) shell> mysql_secure_installation
7) shell> mysql_install_db
8) shell> service mysql status
9) shell> mysqladmin -p -u root version



---------------------------------
ImportError: No module named MySQLdb
$ apt-get install python-mysqldb


---------------------------------
1) mysql> create database vr_server character set utf8 collate utf8_bin;
Query OK, 1 row affected (0.00 sec)
2) mysql> create user 'vr-server'@'127.0.0.1' identified by 'Vr-0#Ser.ver';
Query OK, 0 rows affected (0.00 sec)
3) mysql> grant all privileges on vr_server.* to 'vr-server'@'127.0.0.1' identified by 'Vr-0#Ser.ver';
Query OK, 0 rows affected, 1 warning (0.00 sec)
4) mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)
5) 
