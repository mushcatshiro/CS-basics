[TOC]

# crawling through forms and logins

we have been only dealing with contents that are obtainable through GET requests, but not POSTS / forms. we can enable this by using Requests.

## Basic forms consist of text inputs which can likely be done as shown

`````python
import requests

params = {'field1': 'asdf', 'field2': 'asdf'}
r = requests.post('link', data=params)
`````

## Radio buttons, checkboxes and other inputs

regardless of its complexity, we only need to worry about the name of the element (name attribute) and its value. a dumb way is to submit forms and observe the requests.

## submitting files and images

although is not part of scraping, its possible to be done as follows for testing

````python
files = {'uploadfile': open('file.txt')}
r = requests.post('link', files=files)
````

## logins and cookies

to stay logged-in, we usually uses cookies that is likely server side generated or sort to remain logged in as proof of authentication

````python
r_login = requests.post('url', params=params)
r = requests.get('url', cookies=r_login.cookies)
````

the shown example is for simple situations, there exists sites that frequently updates / modifies cookies without warning (for security / anti-scrapping purposes) or we might want to care-less on this issue, we can do as follows

````python
session = requests.Session()

s = session.post('url', params=params)
# cookies is stored thus,
s = session.get('url')
````

the session object keep tracks on all necessary information including cookies, headers, protocols (eg. HTTP, HTTPAdapters), but keep in mind its not THE solution.

## HTTP basic access authentication

(flask-httpauth)

````python
from requests.auth import AuthBase, HTTPBasicAuth

auth = HTTPBasicAuth('username', 'password')
r = requests.post('url', auth=auth)
````

more forms related topic in Image Processing and Text Recognition chapter and Avoiding Scraping Traps