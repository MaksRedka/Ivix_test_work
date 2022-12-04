import scrapy
import urllib

API_KEY = 'c6155822-a4ae-4663-9bcc-30b040333823'

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urllib.parse.urlencode(payload)
    return proxy_url


class ConstractorSpider(scrapy.Spider):
    name = "constractor"

    def start_requests(self):
        urls = [
            'https://www.yelp.com/search?cflt=contractors&find_loc=San%20Francisco%2C%20CA',
        ]

        for url in urls:
            yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse)


    def parse(self, response):
        for quote in response.css('div.toggle__09f24__aaito'):
                url = 'https://www.yelp.com' + quote.css('a.css-1m051bw::attr(href)').get()
                yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse_page)
        
        next_page = response.css('a.next-link::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


    def parse_page(self, response):
            reviews = []
        
            for index, review in enumerate(response.css('#reviews > section > div.css-79elbk.border-color--default__09f24__NPAKY > div > ul')):
                if index < 5:
                    rew = {
                        'Name': review.css('a.css-1m051bw::text').get(),
                        'Location': review.css('span.css-qgunke::text').get(),
                        'Date': review.css('css.css-chan6m').get(),                
                    }
                    reviews.append(rew)

            yield {
                'Business name': response.css('h1.css-1se8maq::text').get(),
                'Business rating': response.xpath('//*[@id="main-content"]/div[1]/div/div/div[2]/div[1]/span/div/@aria-label').get(),
                'Number of reviews': response.xpath('//*[@id="main-content"]/div[1]/div/div/div[2]/div[2]/span/a/text()').get(),
                'Business yelp url': response.xpath('/html/head/meta[13]/@content').get(),
                'Buines website': response.xpath('/html/body/yelp-react-root/div[1]/div[3]/div/div/div[2]/div/div[2]/div/aside/section[1]/div/div[1]/div/div[1]/p[2]/a/text()').get(),
                'Reviews': reviews
                }        


