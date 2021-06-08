import hashlib
import os 
import sys

from bs4 import BeautifulSoup
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


HTML_EVENT_HANDLERS = [
    "onafterprint",
    "onbeforeprint",
    "onbeforeunload",
    "onerror",
    "onhashchange",
    "onload",
    "onmessage",
    "ononline",
    "onpagehide",
    "onpageshow",
    "onpopstate",
    "onresize",
    "onstorage",
    "onunload",
    "onblur",
    "onchange",
    "oncontextmenu",
    "onfocus",
    "oninput",
    "oninvalid",
    "onreset",
    "onsearch",
    "onselect",
    "onsubmit",
    "onkeydown",
    "onkeypress",
    "onkeyup",
    "onclick",
    "ondblclick",
    "onmousedown",
    "onmousemove",
    "onmouseout",
    "onmouseover",
    "onmouseup",
    "onmousewheel",
    "onwheel",
    "ondrag",
    "ondragend",
    "ondragenter",
    "ondragleave",
    "ondragover",
    "ondragstart",
    "ondrop",
    "onscroll",
    "oncopy",
    "oncut",
    "onpaste",
    "onabort",
    "oncanplay",
    "oncanplaythrough",
    "oncuechange",
    "ondurationchange",
    "onemptied",
    "onended",
    "onerror",
    "onloadeddata",
    "onloadedmetadata",
    "onloadstart",
    "onpause",
    "onplay",
    "onplaying",
    "onprogress",
    "onratechange",
    "onseeked",
    "onseeking",
    "onstalled",
    "onsuspend",
    "ontimeupdate",
    "onvolumechange",
    "onwaiting",
]


class InlineEventHandlerSpider(CrawlSpider):
    name = "event_handler"
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
            seen_event_handlers = set()
            for tag in soup.find_all():
                try:
                    for event_handler in HTML_EVENT_HANDLERS:
                        try:
                            if tag[event_handler] not in seen_event_handlers:
                                seen_event_handlers.add(tag[event_handler])
                                yield {
                                    "url": response.url,
                                    "event_handler": event_handler,
                                    "inline_script": tag[event_handler],
                                    "tag": str(tag),
                                    "tag-sha256": hashlib.sha256(str(tag).encode("utf-8")).hexdigest()
                                }
                        except:
                            pass
                except:
                    pass
        except:
            pass
