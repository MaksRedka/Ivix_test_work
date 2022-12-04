import scrapy
import urllib

API_KEY = 'c6155822-a4ae-4663-9bcc-30b040333823'

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urllib.parse.urlencode(payload)
    return proxy_url



class AllCategorysSpider(scrapy.Spider):
    name = "all_categorys"
    categorys = ['Delivery', 'burgers', 'chinese', 'italian', 'Reservations', 'japanese', 'mexican', 'thai', 'contractors', 'electricians', 'homecleaning',
             'hvac', 'landscaping', 'locksmiths' ,'movers' ,'plumbing' ,'autorepair', 'auto_detailing', 'bodyshops', 'carwash', 'car_dealers', 'oilchange', 'parking', 'towing',
              'dryclean', 'mobilephonerepair', 'bars', 'nightlife', 'hair', 'gyms', 'massage', 'shopping']

    base_url = 'yelp.com'

    def start_requests(self):

        for indx, category in enumerate(self.categorys):
            if indx < 2:
                url = f"https://www.yelp.com/search?cflt={category}&find_loc=San%20Francisco%2C%20CA"
                yield scrapy.Request(url=get_scrapeops_url(url.format(category)), callback=self.parse)


    def parse(self, response):
        i = 0
        for quote in response.css('div.container__09f24__mpR8_'):
                url = 'https://www.yelp.com' + quote.css('a.css-1m051bw::attr(href)').get()
                yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse_page)
        
        next_page = response.css('a.next-link::attr("href")').get()
        if next_page is not None and i < 1:
            i += 1
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
            'Business rating': response.css('div.five-stars__09f24__mBKym::attr(aria-label)').get(),                        
            'Number of reviews': response.css('div.rating-text__09f24__VDRkR p.css-foyide::text').get(),
            'Business yelp url': response.xpath('/html/head/meta[13]/@content').get(),
            'Busines website': response.css('div.css-1vhakgw a.css-1um3nx::text').get(),
            'Reviews': reviews
            }  