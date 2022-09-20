[TOC]

# Crawling in parallel

parallel crawling could get us into trouble if not handled properly.

- collecting from multiple machines
- prolonged / complex operation on collected data + parallel collecting data
- collecting data from large web service where there is an agreement and rapid crawling is authorized

## process vs threads

in CS process on an os can have multiple threads. each process has its own allocated memory, which means multiple can access same memory, but between processes cannot and must communicate information explicitly.

python GIL prevents threads from executing same line of code at once. GIL ensures common memory shared by all processes does not become corrupted.

python 3.X uses _thread module for multithreading purposes.

````python
try:
    _thread.start_new_thread(fn, (**kwargs))
except:
    print('error: unable to start new threads')
while 1:
    pass
````

## race conditions and queues

python list is not a good means of communicating messages, many operation is not thread-safe. the safer option is to move towards a Queue, where is not designed to store static data but to transmit it in a thread-safe way.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random
import _thread
from queue import Queue
import time
import pymysql

def storage(queue):
    conn = pymysql.connect(host='', unix_socket='/tmp/mysql.sock', user='', passwd='', db='', charset='utf8')
    cur = conn.cursor()
    while 1:
        if not queue.empty():
            article = queue.set()
            cur.execute('SELECT * FROM pages WHERE paths = %s', (article['path']))
            if cur.rowcount == 0:
                print(f'storing article {article["path"]}')
                cur.execute('INSERT INTO pages (title, path) VALUES (%s, %s)', (article['title'], article['path']))
                conn.commit()
            else:
                print(f'article already exists {article["title"]}')
visited = []

def getLinks(thread_name, bs):
    print(f'getting links in {thread_name}')
    links = bs.find('div', {'id': 'bodyContent'}).findall('a', href=re.compile('^(/wiki/)((?!:).)*$'))
    return [link for link in links if link not in visited]

def scrape_article(thread_name, path, queue):
    visited.append(path)
    html = urlopen(f'http://en.wikipedia.org{path}')
    time.sleep(5)
    bs = BeautifulSoup(html, 'html.parser')
    titile = bs.find('h1').get_text()
    print(f'added{title} for storage in thread{thread_name}')
    queue.put({'title': title, 'path': path})
    links = getLinks(thread_name, bs)
    if len(links) > 0:
        newArticle = links[random.randint(0, len(links)-1)].attrs['href']
        scrape_article(thread_name, newArticle, queue)
queue = Queue()
try:
    _thread.start_new_thread(scrape_article, ('Thread 1', '/wiki/Kevin_Bacon', queue,))
    _thread.start_new_thread(scrape_article, ('Thread 2', '/wiki/Monty_Python', queue,))
    _thread.start_new_thread(storage, (queue,))
except:
    print('Error: unable to create threads')
while 1:
    pass
```

_thread is a low level module, threading is the higher-level interface that we can utilize. threading module allow us to create a local thread data that is unavailable  to other threads.

```python
import threading

def crawler(url):
    data = threading.local()
    data.visited = []
threading.Thread(target=crawler, args=('http://wikipedia.org')).start()
```

we share only information needed through Queue

```python
threading.Thread(target=crawler)
t.start()

while True:
    time.sleep(1)
    if not t.isAlive():
        t = threading.Thread(target=crawler)
        t.start()
# -----

class Crawler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.done = False
    def isDone(self):
        return self.done
    def run(self):
        time.sleep(5)
        self.done = True
        raise Exception('sth went wrong')
t = Crawler()
t.start()

while True:
    time.sleep(1)
    if t.isDone():
        print('done')
        break
    if not t.isAlive():
        t = Crawler()
        t.start()
```

## multiprocessing crawling

python processing module creates new process objects that can be started and joined from the main process.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random
from multiprocessing import Process
import os
import time

visited = []
def getLinks(bs):
    print(f'getting links in {os.getpid()}')
    links = bs.find('div', {'id': 'bodyContent'}).findall('a', href=re.compile('^(/wiki/)((?!:).)*$'))
    return [link for link in links if link not in visited]

def scrape_article(path):
    visited.append(path)
    html = urlopen(f'http://en.wikipedia.org{path}')
    time.sleep(5)
    bs = BeautifulSoup(html, 'html.parser')
    titile = bs.find('h1').get_text()
    print(f'scraping {title} for storage in process {os.getpid()}')
    queue.put({'title': title, 'path': path})
    links = getLinks(bs)
    if len(links) > 0:
        newArticle = links[random.randint(0, len(links)-1)].attrs['href']
        print(newArticle)
        scrape_article(newArticle)
processes = []
processes.append(Process(target=scrape_article, args=('/wiki/Kevin_Bacon',)))
processes.append(Process(target=scrape_article, args=('/wiki/Monty_Python',)))

for p in processes:
    p.start()
```

multiprocess crawling is theoretically faster due to 

- processes are not subject to locking by GIL and can execute the same lines of code and modify the same object at the same time
- processes can run on multiple CPU cores, it could be advantageous if processes are processor intensive

### communication between processes

to share information between processes in python we can use queues and pipes. queues here are similar to the queue from Queue module where information can be put into it by one process and removed by another process. its design as a method of temporary data transmission thus not well suited to hold static data eg. webpages that have been visited.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random
from multiprocessing import Process, Queue
import os
import time

def task_delegator(taskQueue, urlsQueue):
    visited = ['/wiki/Kevin_Bacon', '/wiki/Monty_python']
    taskQueue.put('/wiki/Kevin_Bacon')
    taskQueue.put('/wiki/Monty_python')
    
    while 1:
        if not urlsQueue.empty():
            links = [link for link in urlsQueue.get() if not in visited]
            for link in links:
                taskQueue.put(link)

def getLinks(bs):
    print(f'getting links in {os.getpid()}')
    links = bs.find('div', {'id': 'bodyContent'}).findall('a', href=re.compile('^(/wiki/)((?!:).)*$'))
    return [link.attr['href'] for link in links]

def scrape_article(taskQueue, urlsQueue):
    while 1:
        while taskQueue.empty():
            time.sleep(0.1)
        path = taskQueue.get()
        html = urlopen(f'http://en.wikipedia.org{path}')
        time.sleep(5)
        bs = BeautifulSoup(html, 'html.parser')
        titile = bs.find('h1').get_text()
        print(f'scraping {title} for storage in process {os.getpid()}')
        links = getLinks(bs)
        urlsQueue.put(links)

processes = []
taskQueue = Queue()
urlsQueue = Queue()
processes.append(Process(target=task_delegator, args=(taskQueue, urlsQueue,)))
processes.append(Process(target=scrape_article, args=(taskQueue, urlsQueue,)))
processes.append(Process(target=scrape_article, args=(taskQueue, urlsQueue,)))

for p in processes:
    p.start()
```

## multiprocessing - another approach

if its not a huge project with any communication between crawler is needed we could simply start multiple python scripts in terminal and let them run (in different processes)