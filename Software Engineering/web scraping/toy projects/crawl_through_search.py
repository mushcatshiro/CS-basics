import requests
from bs4 import BeautifulSoup


class Content():

    def __init__(self, topic, url, title, description):
        self.topic = topic
        self.url = url
        self.title = title
        self.description = description

    def print(self):
        print(f'new article found for topic {self.topic}')
        print(f'title: {self.title}')
        print(f'url: {self.url}')
        print(f'description: {self.description}')
        print()


class Website():
    """docstring for Website"""

    def __init__(self, name, url, searchUrl, resultListing,
                 resultUrl, absUrl, titleTag, descriptionTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absUrl = absUrl
        self.titleTag = titleTag
        self.descriptionTag = descriptionTag


class Crawler():

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            raise None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        return ''

    def search(self, topic, site):
        """
        searches a given website for a given topic and records all result
        """
        bs = self.getPage(site.searchUrl + topic)
        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs['href']
            if site.absUrl:
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print(f'something was wrong with {url}, skipping')
                continue
            title = self.safeGet(bs, site.titleTag)
            description = self.safeGet(bs, site.descriptionTag)
            if title != '' and description != '':
                content = Content(topic, url, title, description)
                content.print()


crawler = Crawler()

siteData = [['O\'Rielly Media', 'http://oreilly.com',
             'http://ssearch.oreilly.com/?q=', 'article.product-result',
             'p.title a', True, 'h1', '.product-description p'],
            ]

sites = []

for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3], row[4],
                         row[5], row[6], row[7]))

topics = ['python', 'data science']

for topic in topics:
    print(f'getting info on topic {topic} \n')
    for targetSite in sites:
        crawler.search(topic, targetSite)

"""
<article class="result product-result">
            <a class="learn-more" href="https://www.oreilly.com/programming/free/python-for-scientists.csp">Learn more</a>
              <a href="https://www.oreilly.com/programming/free/python-for-scientists.csp"> 
                <img src="//akamaicovers.oreilly.com/images/0636920046240/cat.gif" alt="Python for Scientists" class="book">
              </a>
              <div class="book_text">
            <p class="title">
                <a href="https://www.oreilly.com/programming/free/python-for-scientists.csp">
                  Python for Scientists
                </a>
            </p>
              <p class="note">By A publication of O'Reilly Media</p>
              <p class="note publisher">Publisher: O'Reilly Media</p>
                <p class="note date2">Release Date: 
                        September 17, 2015
</p>
              <p class="note">Language: English</p>
              </div><!-- /.book_text -->
            </article>
"""