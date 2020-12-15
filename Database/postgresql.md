[TOC]

# postgresql

linux (ubuntu) install

note: postgres has spec for each ubuntu version, so if we want to install different version we need to check the online step by step guide

```bash
>> sudo apt-get install postgresql
>> service postgres # to see what available cmd combinations
>> ls /etc/postgres/'version'/main/postgresql.conf # main config file to check eg. ports and etc.
>> sudo su postgres # to change to postgres superuser
>> psql # to start psql interactive shell interface
>> \l # list of all db
>> \du # list of all users
```

create / delete users

```sql
ALTER USER postgres WITH PASSWORD 'new password'; -- no flush needed
CREATE USER user_name WITH PASSWORD 'password';
ALTER USER user_name WITH SUPERUSER; -- granting superuser access, check with \du
DROP USER user_name; -- delete user
SHOW config_file;
\password -- to set password
```

or we can create user based on our current account

````bash
>> sudo -u postgres createuser --superuser $USER # create user based on current user
>> $ sudo -u postgres createdb $USER # create database under that user
>> psql # and we can use psql terminal
>> systemctl postgres reload
````

MISC

```sql
SELECT * FROM pg_settings WHERE name = 'port';
SHOW hba_file;
SHOW config_file;
```

configs (hba_config)

```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# IPv6 local connections:
host    all             user_name       0.0.0.0/0               md5
```

config (postgresql.conf)

```
listen_address = '*'
```

Postgresql warning: "could not flush dirty data: Function not implemented"

```bash
>> sudo vi /etc/postgresql/11/main/postgresql.conf
fsync = off # i didn't turn off for this
data_sync_retry = true
```



manual: man psql

pgadmin - gui for psql

[NTU help](https://www3.ntu.edu.sg/home/ehchua/programming/sql/PostgreSQL_GetStarted.html)

