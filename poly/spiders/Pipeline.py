import scrapy
from w3lib.html import remove_tags

class PipelineSpider(scrapy.Spider):

    name = "Pipeline"
    start_urls = [
        'https://poly.rpi.edu/archives/'
    ]


    def parse(self, response):

        if (response.url == "https://poly.rpi.edu/archives/"):
            rel_links = response.css("section.content a.px-2::attr(href)").extract()
            for link in rel_links:
                yield scrapy.Request(url=response.urljoin(link))
                
        elif (response.css("h1 a::text").extract_first() == "Archives"):
            rel_links = response.css("h3.headline a::attr(href)").extract()
            for link in rel_links:
                yield scrapy.Request(url=response.urljoin(link))
        
        else:
            yield {
                'section': response.css("a.active::text").extract_first(),
                'kicker': response.css("strong.text-kicker::text").extract_first(),
                'headline': remove_tags("".join(response.css("h1.article-headline").re(r'<h1.*?>(.*?)<\/h1>'))),
                'author': remove_tags(response.css("span.authors .author-name").extract_first()),
                'posted-date': response.css("a.published-date::text").extract_first().strip(),
                 
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
