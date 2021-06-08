import hashlib
import os 
import sys

from bs4 import BeautifulSoup
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class InlineCssSpider(CrawlSpider):
    name = "css"
    rules = (
        Rule(LinkExtractor(allow=(), deny=("\?", "\|", "\%7C")), callback="parse", follow=True),
    )

    def __init__(self, urls, domains, **kwargs):
        self.start_urls = []
        with open(urls, "r", encoding="utf-8") as fp:
            for line in fp:
                self.start_urls.append(line.strip())

        self.allowed_domains = []
        with open(domains, "r", encoding="utf-8") as fp:
            for line in fp:
                self.allowed_domains.append(line.strip())

        super().__init__(**kwargs)

    def parse(self, response):
        try:
            soup = BeautifulSoup(response.body, "html.parser")
            seen_css = set()
            for tag in soup.find_all():
                try:
                    if tag["style"] not in seen_css:
                        seen_css.add(tag["style"])
                        yield {
                            "url": response.url,
                            "inline-css": tag["style"],
                            "tag": str(tag),
                            "tag-sha256": hashlib.sha256(str(tag).encode("utf-8")).hexdigest()
                        }
                except:
                    pass
        except:
            pass
