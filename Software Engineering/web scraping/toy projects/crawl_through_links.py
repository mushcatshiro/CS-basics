import requests
from bs4 import BeautifulSoup
import re


class Content():

    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def print(self):
        print(f'title: {self.title}')
        print(f'url: {self.url}')
        print(f'description: {self.description}')
        print()


class Website():
    """docstring for Website"""

    def __init__(self, name, url, targetPattern,
                 absUrl, titleTag, descriptionTag):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absUrl = absUrl
        self.titleTag = titleTag
        self.descriptionTag = descriptionTag


class Crawler():

    def __init__(self, site):
        self.site = site
        self.visited = []

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            raise None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            # should be catering for multiple same selector on a single page
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.titleTag)
            description = self.safeGet(bs, self.site.descriptionTag)
            if title != '' and description != '':
                content = Content(url, title, description)
                content.print()

    def crawl(self):
        """
        searches a given website for a given topic and records all result
        """
        bs = self.getPage(self.site.url)
        targetPages = bs.find_all('a',
                                  href=re.compile(self.site.targetPattern))
        for targetPage in targetPages:
            targetPage = targetPage.attrs['href']
            if targetPage not in self.visited:
                self.visited.append(targetPage)
                if not self.site.absUrl:
                    targetPage = f'{self.site.url}{targetPage}'
                self.parse(targetPage)
            break


reuters = Website('Reuters', 'https://www.reuters.com', '^(/article/)',
                  False, 'h1', '.StandardArticleBody_body')

crawler = Crawler(reuters)
crawler.crawl()


"""
<div class="StandardArticleBody_container"><div class="StandardArticleBody_body"><p>JOHANNESBURG (Reuters) - Democratic Republic of Congo mines minister Willy Kitobo Samsoni plans to meet with mining companies to agree a moratorium on confining workers to mine sites due to the coronavirus. </p><p>Civil society groups last month demanded an end to mandatory mine-site confinement policies put in place by copper and cobalt mining companies to avoid coronavirus outbreaks. </p><p>Samsoni said in a statement released on Sunday that he would engage with mining companies and deliver a moratorium to them in order to end confinement while taking into account their individual needs. </p><div><div class="DPSlot_container StandardArticleBody_dp-slot-inline StandardArticleBody_inline-canvas"><div class="DPSlot_slot" id="dpslot_canvas_8707722_USKBN2460FD"></div></div></div><div><div class="DPSlot_container StandardArticleBody_dp-slot-inline"><div class="DPSlot_slot" id="dpslot_native_1101600_USKBN2460FD"></div></div></div><p>All mining firms must find “appropriate solutions in order to protect both the economy, and the workers who have been separated from their families for a long time,” Samsoni said. </p><p>Samsoni, speaking in the heart of Congo’s copper belt, also touched on the difficulties the pandemic has caused for the mining sector, a critical part of the economy which generated 32% of GDP and 95% of export revenue in 2018. </p><p>“Coronavirus has dealt a fatal blow to mining activities, with the impossibility of repatriating capital, importations of products for the industry coming to a halt, the dizzying drop in metals prices on global markets in March,” he said. </p><div class="Attribution_container"><div class="Attribution_attribution"><p class="Attribution_content">Reporting by Hereward Holland and Helen Reid; Editing by Alexander Smith</p></div></div><div class="StandardArticleBody_trustBadgeContainer"><span class="StandardArticleBody_trustBadgeTitle">Our Standards:</span><span class="trustBadgeUrl"><a href="http://thomsonreuters.com/en/about-us/trust-principles.html">The Thomson Reuters Trust Principles.</a></span></div></div><div><div class="DPSlot_container StandardArticleBody_dp-slot-inline"><div class="DPSlot_slot" id="dpslot_connatix_2401865_USKBN2460FD"></div></div></div><span> </span><oovbm id="igkCeqbK"><div style="     background-color: #fff;     height: auto;     display: table;     font-family: sans-serif;     position: relative; "> <div class="line2" style="     font-family: knowledge-medium, sans-serif;     padding-top: 5px;     -webkit-font-smoothing: antialiased;     font-size: 12px;     color: #86888b;     text-transform: uppercase;     margin-bottom: 20px;     text-align: left;     border-top: 1px solid #d2d2d2;     display: block;     width: 755px;     letter-spacing: 3.25px; ">Paid Promotional Links</div> <div class="sponsor"> <div class="sub-line2" style="     color: #999;     display: block;     font-size: 12px;     overflow: hidden;     padding-bottom: 0;     position: absolute;     right: 0;     top: 6px;     font-weight: 400;     z-index: 1;     width: 120px;     font-size: 12px;     -webkit-font-smoothing: antialiased;     font-family: knowledge-medium, sans-serif; ">Promoted by&nbsp;&nbsp;<a href="https://www.dianomi.com/whatsthis.pl?id=4765" target="_blank" style="     font-size: 12px;     color: #999;     text-decoration: underline;     font-weight: 600; ">Dianomi</a> </div> <a href="https://www.dianomi.com/whatsthis.pl?id=4765" target="_blank" class="dianomihref"> </a> </div> </div><div id="bCRZLhIp" class="VwuxQj "></div><div class="sfbobj0"> </div><div class="sfbobj1"> </div><div class="sfbobj2"> </div><div class="sfbobj3"> </div><div class="sfbobj4"> </div><div class="sfbobj5"> </div><div class="sfbobj6"> </div><div class="sfbobj7"> </div><div class="sfbobj8"> </div><div class="sfbobj9"> </div><div></div></oovbm><div class="StandardArticleBody_dp-slot-inline"><div><div class="CanvasAd_container CanvasAd_collapsed"><p>Advertisement</p><div id="canvas_mobile_leaderboard_4144747194293101_USKBN2460FD" class="CanvasAd_slot"></div></div></div></div><div><div class="DPSlot_container StandardArticleBody_dp-slot-inline"><div class="DPSlot_slot" id="dpslot_connatix_1805553_USKBN2460FD"></div></div></div><div class="StandardArticleBody_dianomi-container dianomi_context" data-dianomi-context-id="4"><script src="https://www.dianomi.com/js/contextfeed.js?" id="dianomi_context_script" type="text/javascript"></script></div></div>
"""