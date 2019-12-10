import scrapy
from w3lib.html import remove_tags

class OnlineSpider(scrapy.Spider):

    name = "Online"
    start_urls = [
        'https://poly.rpi.edu/archives/'
    ]


    def parse(self, response):
        
            yield {
                'section': response.xpath("//table//b[1]//font/text()").extract_first(),
                'kicker': "",
                'headline': response.xpath("//table//b[2]//font/text()").extract_first(),
                'author': response.xpath("//table//b[3]//font/text()").extract_first(),
                'posted-date': "".join(response.xpath("//table//tr[1]/td/i/font/text()").re("Posted (.*) at .*")),
                 
                'has-featured-photo': response.css("div.featured-photo img::attr(src)").extract_first() is not None,
                'featured-photo-photographer': response.css("div.featured-photo span.small a::text").extract_first(),
                'featured-photo-caption': remove_tags("".join(response.css("span.caption").re(r'<span.*?>(.*?)<\/span>'))),
                
                'num-gallery-photos': len(response.css("div.photo-gallery div.photo").extract()),
                'gallery-photographers': response.css("div.photo-gallery div.photo img::attr(data-photographer)").re(r'<a.*>(.*?)<\/a>'),
                'gallery-captions': response.css("div.photo-gallery div.photo img::attr(data-caption)").extract(),
                
                'num-block-photos': len(response.css("div.photo-block").extract()),
                'block-photographers': response.css("div.photo-block div.container span.small a::text").extract(),
                'block-captions': response.css("div.photo-block div.container span.caption::text").extract(),
                
                'body': remove_tags(" ".join(response.css("div.body p").extract())).replace("\n", ''),
                
                'url': response.url
            }
