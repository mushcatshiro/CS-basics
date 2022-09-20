[TOC]

# Basic Crawling

the UR^2^IM approach

- url
- request
- response
- items
- more urls

start scrapy project (from scratch)

```bash
>> scrapy startproject project_name
>> cd project_name
>> tree
.
| - projectname
| | - __init__.py
| | - items.py
| | - pipelines.py
| | - settings.py
| | - spiders
| | | - __init__.py
| | - scrapy.cfg
```

in this chapter we will only work with items.py and spiders directory.

## defining items in items.py

fields we declared is can be left empty. usually there are 3 main field types, primary, calculated, and housekeeping fields.

housekeeping fields - not application-specific, usually helps in debug and / or logging

- url - response url
- project - project name
- spider - self.name
- server - host name?
- date - datetime.datetime.now()

```bash
# creating a basic non-cross domain spider (under same project)
>> scrapy genspider basic target_site # eg. google
```

check the basic.py file and we can see parse function with response as a input parameter, its basically the response object from our request. in parse function we can specify what we would like to do with the url response.

```bash
>> scrapy crawl basic # to run
>> scrapy parse --spider=basic http://url
```

using scrapy parse allow us to use the most suitable spider to parse **any url given**. parse is a tool for debugging

## populating an item

by importing the item object we configured in items.py to parse function we could then pipe and export the information in different formats and export to different places.

we could pipe through -o option as shown

```bash
>> scrapy crawl basic -o items.json # .csv and etc
```

note: json file type will be accumulating everything in a huge array in memory when we try to read and parse it, using .jl file we have one json object per line thus read efficiency.

we could also pipe to our FTP servers or services eg.

```bash
>> scrapy crawl basic -o "ftp://user:pass@ftp.scrapybook.com/items.json" # or
>> scrapy crawl basic -o "s3://aws_key:aws_secret@scrapybook/items.json"
```

there is lack of built in support to RDBMS due to performance bottleneck while scrapy is meant for efficiency. we will revisit this topic in pipeline chapter.

## cleaning up fields

instead of

```python
item = ToyspiderItem()
self.log(f"""url:
            {response.xpath('//*[@itemprop="url"][1]/text()').extract()}""")
item['url'] =\
	response.xpath('//*[@itemprop="url"][1]/text()').extract()
```

we could do something like

```python
    l = ItemLoader(item=ToyspiderItem(), response=response)
    l.add_xpath('url', '//*[@itemprop="url"][1]/text()')
return l.load_item()
```

ItemLoader provides ways of combining, formatting and cleaning data. ItemLoader pass values to various processor classes, which is some fast and simple functions, a few to show

| processor  | functionality         |
| ---------- | --------------------- |
| Join       | join multiple results |
| MapCompose |                       |
|            |                       |
|            |                       |
|            |                       |

MapCompose can be used with any python function or chain of python function to implement functionality.