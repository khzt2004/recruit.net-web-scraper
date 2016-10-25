# encoding=utf-8
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from recruitnet.items import RecruitnetItem
import re
import sys

### Kludge to set default encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

class MySpider(CrawlSpider):
    name = "recruit"
    allowed_domains = ["australia.recruit.net"]
    start_urls = [
    "http://australia.recruit.net/search.html?jobRef=&query=plm&location=&postdate=&hitsPerPage=10&totalPages=5&dedup=true&sortby=relevance&pageNo=1&f_region=&f_title=&f_location=&f_company=&newjobs=false&filter_company=false&filter_agency=false&companysite_filter=false&dup=&distance=&phrase=&orwords=&notwords=&jobtitle=&company=&f_type=&f_source=&f_salary=&f_experience=&s="
    ]
    download_delay = 3

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="pagination hidden-phone"]/ul/li[@class="next"]/a',)), callback='parse_item', follow=True),
        )

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        for quote in response.xpath('//div[contains(@class, "job organic")]'):
        	item = RecruitnetItem()
        	item['title'] = quote.xpath('./h2/a/@title').extract()
        	item['link'] = quote.xpath('./h2/a/@href').extract()
        	item['company'] = quote.xpath('./div[1]/h3/span[1]/a/span/span/text()').extract()
        	item['location'] = quote.xpath('./div[1]/h3/span[2]/span/span/text() | ./div/h3/span[@class="location"]/text()').extract()
        	yield item