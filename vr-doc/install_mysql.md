do it as 
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-14-04
http://www.devopsservice.com/installation-of-mysql-server-5-7-on-ubuntu-14-04/

root/abcd.1234
----------------------------------
1) shell> sudo wget http://dev.mysql.com/get/mysql-apt-config_0.6.0-1_all.deb
2) shell> sudo dpkg -i mysql-apt-config_0.6.0-1_all.deb
3) shell> sudo apt-get update
4) shell> sudo apt-get install mysql-server
5) shell> sudo mysql_secure_installation
6) shell> sudo mysql_install_db
7) shell> sudo service mysql status
8) shell> sudo mysqladmin -p -u root version
9) root: henG!@#32032


---------------------------------
ImportError: No module named MySQLdb
$ sudo apt-get install python-mysqldb


---------------------------------
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
