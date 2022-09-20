[TOC]

# Scraping remotely

why remote?

- power and flexibility
- alternate IP address

## avoiding IP address blocking

building web scrappers, everything can be faked, but not IP address. thus most effort of stopping scrappers is to block IP address.

- this might not be a good solution, every big company would need to maintain a huge list of blacklisted IP
- to make the blocking less troublesome and to reduce the amount of processing power wasted on blocking IP, usually IP blocking would be that IP address and eg. +- 256 addresses in the range together
- this could cause accidental blocking normal users

## portability and extensibility

some task is too huge for personal computer to handle and freeing up your own processing power is always a good thing (task delegation). besides pc uptime and network maintenance will no longer be a concern. also distributed computing is possible with multiple say amazon instance

## TOR

limitation of anonymity - its not an invisibility cloak, there is no way to achieve complete anonymity.

## pysocks

python module that is capable of routing traffic through proxy servers and can be work in conjunction with TOR. TOR service must be running on 9150 port thus

```python
import socks
import socket
form urllib.request import urlopen
socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket
print(urlopen('link'.read()))
```

to use selenium and phantomJS with tor, there is no need of pysocks, just need to ensure tor is running 

```python
from selenium import webdriver

service_args = ['--proxy=localhost:9150', '--proxy-type=socks5',]
driver = webdriver.PhantomJS(executable_path='path', sercice_args=service_args)
driver.get('http://icanhazip.com')
print(driver.page_source)
driver.close()
```

## remote hosting

hosting on eg. amazon service means you lost your anonymity when the bill is paid but it improves scrapers speed.