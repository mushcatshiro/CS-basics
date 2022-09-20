[TOC]

# Scrapy

## 1. introduction to scrapy

> more to read in learning scrapy, o'reilly

```bash
scrapy startproject yourprojectname
```

- for each spider we create a object and inherit from scrapy.Spider.
- basic functions include start_requests and parse
- start_requests is a scrapy defined entry point to generate request object to crawl website
- parse is a callback defined by user passed to request object

## 2. spidering with rules

a real spider should at least be able to discover new URL on it self and collect information. to enable this scrapy provided a CrawlSpider class. instead of providing a start_request function, we can provide a list of start_urls and allowed_domain. this provides the spider a starting point and a set of rules to follow or to not follow a URL.

XPath selector can be used to extract each page. XPath allows us to collect text content including text in child tags compared to CSS selectors.

| Spider                                                       | CrawlSpider                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| simplest spider                                              | one of the generic spider                                    |
| every other spider must inherit from (including custom ones) | can be inherited, aim to provide functionality for common scarping cases |
| default start_requests which sends requests from start_urls and calls spider method parse for each responses | rules must be provided as list, if multiple satisfied, the **first **one will be used |

> Warning: articles.py will run forever, remember to halt, also why / how it run? (involvement of stack / queue?)

crawling rules

- link_extractor is required
- callback: to avoid callback function name 'parse'
- cb_kwargs
- follow: links found to be crawled in the future, if callback if provided it is defaulted to false, else its true

link extractor, a class designed to recognize and return links in a HTML page

- allow: regex of the absolute urls must be matched
- extandable

``````python
# crawling with more rules example
# ...
    rules = [
        Rule(LinkExtractor(allow='^(/wiki/)((?!:).)*$'),
             callback='parse_items', follow=True,
             cb_kwargs={'is_article': True}),
        Rule(LinkExtractor(allow='.*'),
             callback='parse_items',
             cb_kwargs={'is_article': False}) # how is this achieved? string to function/variable name matching
    ]

def parse_items(self, response, is_article):
    print(response.url)
    title = response.css('h1::text').extract_first()
    if is_article:
        url = response.url
        text = response.xpath('//div[@id="mw-content-text"]//text()').extract()
        lastUpdated = response.css('li#footer-info-lastmod::text').extract_first()
        lastUpdated = lastUpdated.replace('This page was last edited on ', '')
        print(f"""
        	title: {title}
        	url: {url}
        	text: {text}
        	lastUpdated: {lastUpdated}
        """)
    else:
        print(f'this is not an article: {title}')
``````

> the approach provided above is impractical, instead ignore all those that doesn't match to the article page pattern

## 3. creating items

scrapy provides tool to keep collected item organized and stored in custom objects with well defined fields. check under the items.py

``````python
import scrapy

class Article(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    lastUpdated = scrapy.Field()
``````

if the items are large (?), or starting to move more parsing functionality into your item objects you may wish to extract each item into its own file (?)

``````python
from wikiSpider.items import Article

def parse_items(self, response, is_article):
    article = Article()
    article['url'] = response.url
    # ...
    return article # must return the item, and can only return the item
``````

scrapy items not only provides organization to code but also providing functionality for outputting and processing data. it can be used to determine which pieces of information it should save from pages it visits and saved into common file formats including csv, json and xml.

```bash
scrapy runspider articleItems.py -o articles.csv -t csv
```

### 3.1 the item pipeline

scrapy is single threaded, however it is capable of making and handling requests asynchronous. however this will cause surge of load to the web server we are scraping to, and modern web servers have the ability to block what they think is a malicious scraping activity. the main feature of the item pipeline is the improve performance by performing data processing while waiting for request to be returned rather than waiting for data to be processed before making another requests. this makes a difference especially when we are performing a processor heavy calulations.

revisit the settings.py file for the configuration

```python
# uncomment ITEM_PIPELINES
ITEM_PIPELINES = {
    'wikiSpider.pipelines.WikispiderPipeline': 300,
}
```

this provides a class that will be used to process data and as well as an integer that represents the order in which to run the pipeline if there are multiple processing classes (?) we can have multiple pipelines with different tasks however it parses regardless of item type thus item specific parsing is better handled in spider before data hits pipeline (? not shown here) or we can do inside the pipeline if the parsing takes a long time

```python
# in pipelines we declare our pipeline processing

class WikispiderPipeline(object):
    def process_item(self, article, spider):
        if isinstance(item, Article):
        # ...
        return article
```

with this we have to checkpoint to process the scraped information, pipeline or parse_items().

## 4. logging with scrapy

level of logging can be modified in settings.py, logging levels is same as build-in logging