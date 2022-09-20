[TOC]

# storing data

automated data storage. we can store media files by reference or by downloading it.

by reference

| upside                 | downside                                             |
| ---------------------- | ---------------------------------------------------- |
| less bandwitth         | hotlinking to the URL                                |
| less storage required  | relies on external location static-ness              |
| code is much simple    | not downloading make alert web servers you are a bot |
| reduces load on server |                                                      |

usually if the data is viewed frequently then its better off to download it。 however take note, crawler will download anything thus robust extension checking and limited access account is needed in place to protect the server.

## 1. storing to csv

this is different from downloading a csv file, but instead is to scrape certain information, process and store it in csv format. we can utilize the csv library or pandas to do the necessary processing.

```python
# ...
table = bs.findAll('table', {'class': 'wikitable'})[0]
rows = table.findAll('tr')
```

## 2. storing to RDBMS (MySQL)

[SQL](..\storing information\SQL)

```python
import pymysql

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', # the much missed out part
                       user='root', password=None, db='mysql', charset='utf8') # take into consideration
```

Mysql does not handle unicode, thus need to manually turn on this feature (increase db size). utf8mb4 has bad support for unicode.

````sql
ALTER DATABASE dbname CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE pages CONVERT TO CHARACTER SET utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE pages CHANGE title title VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE pages CHANGE content content VARCHAR(100000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
````

choices of choosing PK, to create an id or use unique attribute (we will never be sure of something is truly unique). autoincrement id as primary key. also use indexing (?)

```sql
CREATE INDEX definition on dictionary (id, definition(16));
```

## 3. email

assuming we have access to a server running SMTP client. (remote or local)

```python
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('email body')
msg['Subject'] = 'email subject'
msg['From'] = 'a@b.com'
msg['To'] = 'c@d.com'

s = smtplib.SMTP('localhost')
s = send_message(msg)
s.quit()
```

MIMEText (multipurpose internet mail extensions) object uses MIME protocol (a low level protocol) across SMTP (higher level) connection that have been made.