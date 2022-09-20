[TOC]

# web crawling models

by learning common models / pattern from large scalable crawlers, we can ensure our crawler robustness and maintainability.

## 1 planning and defining objects (data models)

we often create an python object to store information and update to database. however if we ask the question "what exists?" we will get into the trouble of updating the object and database schema. instead ask "what do I need?"

questions to ask

- does this information worth the time collecting? how impactful it will be if we are not collecting it?
- if it might help in the future, how difficult is it for me to go back and collect at a later time?
- is it redundant ie can be interpolate with current collecting data
- does it make sense to store these data in a single object
- is it sparse or dense (ie electronics is a big dense category but asus laptop is a sparse category)
- data size
- scheduled retrieval frequency
- how fast this data varies?

if we are separating out the information into two objects, how to deal with the interaction ie s size shirt and m size shirt having different price (product object and attribute object)

> we might consider to create two product, s size and m size

```python
class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body
    
    def print(self):
        print(f'url: {self.url}')
        print(f'title: {self.title}')
        print(f'body: {self.body}')

class Website:
    def __init__(self, name, url, titleTag, bodyTag):
        
class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')
    
    def safeGet(self, pageObj, selector):
        """
        utility function to get content string from bs object and a selector
        returns empty string if no selector is found in the object 
        """
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''
    
    def parse(self, site, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.titleTag)
            body = self.sageGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(url, title, body)
    
    crawler = Crawler()
    siteData = [['O\'Rielly Media', 'http://shop.oreilly.com/product/', 'h1', 'section#product-description'],
                ['Reuters', 'http://www.reuters.com/article/', 'h1', 'div.StandardArticleBody_body_1gnLA']]
    websites = []
    for row in siteData:
        websites.append(Website(row[0], row[1], row[2], row[3]))
    crawler.parse(websites[0], 'http://shop.oreilly.com/product/0636920028154.do')
```

above is one approach, by providing a flexible structure. in contrast we could have create multiple functions targeted specifically for a site ie getOreilly, getReuter etc. the upside of having a flexible structure is that the siteData can be loaded from a database and can be updated easily through SQL.

## 2. Crawling through search

a common approach that mimics human, through **keywords** or **topic** and collecting a list of search result. it may seems like there is task variability from site to site, however

- most site retrieve search result by passing the topic as a string through a parameter in the URL ie http:google.com?search=myTopic
- after searching the resulting page usually have a identifiable text *results* or tag that contains class = 'result', which can be stored as a property 
- each result can be either a relative URL or absolute URL which can be stored in the Website object as a property
- once the URL is retrieved and normalized, we can scrape it with the code above

[code 01](./crawl_through_search.py)

> practice 01: make code 01 work

## 3. crawling through links

works well if we wanted to get information of an entire website (internal website, also how to differentiate between internal and external?). doesn't require a structured method of locating links like selectors, however we must provide a set of rules to tell it how to select a page

[code 02](.\crawling_through_links.py)

> what's the upside and downside of having website object a property of crawler object itself?

## 4. crawling multiple page types

a few ways to identify a page type

- by URL, ie /some domain/something else/something else
- by presence of absence of certain field on a site, ie. a page with date but no author might be a press release etc.
- by presence of certain tags ie. <div id='something else'>

for the previous examples we only have a single website object, we may want to consider to have multiple given if the page types are drastically different

> OOP concept

``````python
class Website:
    def __init__(self, name, url, titleTag):
        # pass

class Product(Website):
    def __init__(self, name, url, titleTag, productNumber, price):
        Website.__init__(self, name, url, titleTag)
        self.productNumber = productNumber
        self.price = price
``````

## 4. why models

collecting information from internet can be like drinking from fire hose (o'reilly web scraping with python)

- always try to minimize the programming overhead required to add new sources / fields
- normalize the data such that we are dealing with data with identical and comparable fields instead of data that is completely dependent on the format of its original source
  - does this just means to transform the data before loading?
  - or this is referring to database normalization