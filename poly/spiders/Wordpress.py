import scrapy
from w3lib.html import remove_tags

class WordpressSpider(scrapy.Spider):

   name = "Wordpress"
   start_urls = ["https://poly.rpi.edu/" + str(x) + "/" for x in range(2001,2018)]


   def parse(self, response):

      if (response.css("h1.page-title").extract_first() is not None):
         links = response.css("div.posts div.post h2.entry-title a::attr(href)").extract()
         for link in links:
            yield scrapy.Request(url=link)
         next_page = response.css("div.nav-previous a::attr(href)").extract_first()
         if next_page is not None:
            yield scrapy.Request(url=next_page)
      elif (response.css('div.entry-meta a[rel="category tag"]::text').extract_first().lower() == "pdf archives"):
         pass
      else:
         yield {
            'section': response.css('div.entry-meta a[rel="category tag"]::text').extract_first(),
            'kicker': response.css("div.kicker::text").extract_first(),
            'headline': response.css("h1.entry-title::text").extract_first(),
            'author': remove_tags("".join(response.css("div.entry-meta span.name").extract())),
            'posted-date': response.css("div.entry-meta span.entry-date::text").extract_first(),
            
            'has-featured-photo': response.css("div.entry-content div.photo").extract_first() is not None,
            'featured-photo-photographer': response.css("div.entry-content div.photo div.byline::text").re_first(r"(.*)\/"),
            'featured-photo-caption': response.css("div.entry-content div.photo::text").extract_first(),
            
            'num-gallery-photos': len(response.css("div.gallery div.gallery-item").extract()),
            'gallery-photographers': [response.css("div.entry-content small::text").extract_first()],
            'gallery-captions': "",
            
            'num-block-photos': 0,
            'block-photographers': [],
            'block-captions': [],
            
            'body': remove_tags(" ".join(response.css("div.entry-content p").extract())).replace("\n", ''),
            
            'url': response.url
         }

    