[TOC]

#  basic understanding for web scraping

## 1. client and server communication 

````sequence
client->router: header that contains \n destination server IP
router->server:interpret as packet \n stamp own IP \n send to server
note right of server: reads the packet port destination \n pass to appropriate application \n application parsing \n located correct resource and revert
````

## 2. BS4 introduction

```python
from bs4 import BeautifulSoup
import requests as r

resp = r.get('some/domain/name')
resp = BeautifulSoup(resp, 'html.parser') # html object or html string and a parser
```

there are a few html parser, including lxml and html5lib where the prior has better speed and the latter is extremely forgiving

## 3. simple error handling

```python
from urllib3.exceptions import HTTPError

# HTTPError object can be use as a base error object (seen in requests)
# requests has its own set of exceptions

# for connection
try:
    # request
except HTTPError as e:
    print(e)
else:
    # do something
    
# for parsing we would like to check if a certain tag exists by actually accessing it
# if it does not exist a none object will be returned
```

## 4. advanced html parsing

### 4.1 tag based search

- look for unique selectors
- look for alternative source that provides the same data

````python
resp = BeautifulSoup(resp.read(), 'html.parse')
someList = resp.find_all('span', {'class': 'green'}) # tag name and tag attribute
for something in someList:
    name.get_text() # get text strips away all tags, usually is the last step before loading data
````

a full overview of most used two function find and find_all, where find_add(tag, attributes, recursive, text, limit, keywords) and find is limit = 1. keywords most of the time is redundant as we can use regular_express and lambda_express to achieve same results. for tags we pass a list ('or' filtering), and we use keywords in this case for an 'and' filtering

### 4.2 location / hierarchy based search

by traversing the html tree, ie resp.body.span.tr.th

bs4 always deals with the *descendants* of current tag, to target only children

```python
resp.find('table', {'id': '1'}).children
```

dealing with siblings with .next_siblings(), usually used for tables. take note of the 'next', because object cant be the siblings of itself thus the first selected object will be *ignored*. also there exists a .previous_siblings function. dealing with parents is less common but same logic can be applied.

### 4.3 attribute based search

accessing list of attributes, ie resp.img.attrs['src']

### 4.4 lambda expressions

restriction: only takes (html) tag object as an arguments and returns bool

````python
resp.find_all(lambda tag: len(tag.attrs) == 2)
# or
resp.find_all(lambda tag: tag.get_text() == 'some string that you are looking for')
````

## 5. traversing

the six degree of wikipedia: you can reach anything within six intermediary (or less). using wikipedia as an example, if we would like to extract only the *useful* links (ie non main page / contact us etc.) we can use regex for filtering as shown.

````python
for link in resp.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$')):
    if 'href' in link.attrs:
        print(link.attrs['href'])
# (?!:) ?! is a negative lookahead (or (?=:) positive lookahead) meaning it *asserts* no matches return with :
````

> practice 01: build a crawler that crawls all image on a given wikipedia url (psycho-pass)

````python
def crawl_wikipedia_page(wikipedia_link):
    try:
        resp = r.get(wikipedia_link)
    except r.exceptions.RequestException as e:
        raise SystemExit(e)
    else:
        crawl_page_image(resp.text)

def crawl_page_image(html_body):
    resp_cleaned = b(html_body, 'html.parser')
    
    for image in resp_cleaned.find('div', {'id': 'bodyContent'}).find_all('img'):
        fname = image.attrs['src'].split('/')[-1]
        url = image.attrs['src']
        try:
            with open(fname, "wb") as f:
                resp = r.get(f'http:{url}')
                f.write(resp.content)
        except Exception as e:
            with open('log.txt', 'w') as f:
                f.write(f'exception {e} is raised')
````

> practice 02: random crawling

### 5.X deep and dark web

deep web are part of internet that are not indexed by search engines, ie those behind forms / auth and auth etc, which consist of 90% of the web. dark web is a different concept. its running over the current network hardware infrastructure but uses a *client* like Tor with an additional protocol runs on top of HTTP thus providing extra security.

### 5.X calculations

given a website with every page consist of 10 links (unique) and the entire website is 5 pages deep, what is the total number of pages of this page?

> 10^5, (challenge, why its not 10^0 + 10^1 + ... 10^5)

### 5.1 concept of crawling entire website (recursion)

```flow
home=>start: starting link, init set
end=>end: end
op1=>operation: registers all link on current page
op2=>condition: is it already in the set?
op3=>condition: is there any unexplored page?
home->op1->op2
op2(yes)->op3
op2(no)->op1
op3(yes)->op1
op3(no)->end
```

> recursion warning: python recursion depth is 1000
>
> also beware of redirects, if we would like to allow redirects with requests library, we need to set allow_redirects=True