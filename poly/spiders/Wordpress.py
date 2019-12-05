import scrapy
from w3lib.html import remove_tags

class WordpressSpider(scrapy.Spider):

    name = "Wordpress"
    