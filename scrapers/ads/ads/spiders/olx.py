import logging

from scrapy.spiders import Spider
from scrapy.http import Request
from items import AdItem


logger = logging.getLogger(__name__)


class OlxSpider(Spider):

    name = 'olx'
    domain = 'olx.ro'
    allowed_domains = [domain]
    start_urls = ['https://www.olx.ro/oferte/']

    def parse(self, respone):
        # Go for each ad first
        page_urls = respone.xpath("//a[contains(@class, 'detailsLink')]/@href")

        if not page_urls:
            logger.error('Did not find urls on list page')
            return

        for url in page_urls.extract():
            yield Request(url, callback=self.parse_ad, priority=50)

        # Turn to pagination
        pagination_section = respone.xpath("//div[contains(@class, 'pager')]")
        current = pagination_section.xpath(
            ".//span[contains(@class, 'current')]//text()")
        rest = pagination_section.xpath(
            ".//a[contains(@class, 'lheight24')]//text()")

        if not all([pagination_section, current, rest]):
            self.logger.error('Could not parse pagination')
            return

        current_no = int(current[0].extract())
        rest_nos = map(int, rest.extract())

        if current_no + 1 in rest_nos:
            url = self.get_url_for_page(current_no + 1)
            yield Request(url, priority=25)

    def get_url_for_page(self, page):
        return "https://www.olx.ro/oferte/?page={}".format(page)

    def parse_ad(self, respone):
        pass
