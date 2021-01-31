from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.background import BackgroundTask
from starlette.status import HTTP_202_ACCEPTED
import asyncio
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from multiprocessing import Process


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        self.log("I just fisited: " + response.url)
        for quote in response.css("div.quote"):
            yield {
                "author_name": quote.css("small.author::text").get(),
                "text": quote.css("span.text::text").get(),
                "tags": quote.css("a.tag::text").getall(),
            }
        next_page_url = response.css("li.next > a::attr(href)").get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)


async def run_crawler(request):
    data = await request.json()
    query = data['query']
    task = BackgroundTask(crawl, query=query)
    message = {'status': f'Crawler was scheduled with {query=}'}
    return JSONResponse(message, status_code=HTTP_202_ACCEPTED, background=task)


# first test with async tasks
# async def crawl(query):
#    await asyncio.sleep(5)
#    print('Crawler finished!')


# raise error.ReactorNotRestartable()
# async def crawl(query):
#    process = CrawlerProcess()
#    process.crawl(QuotesSpider)
#    process.start()
#    print('Crawler finished!')
install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')

async def crawl(query):
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start(stop_after_crawl=False)
    print(f'Crawler {query=} finished!')

routes = [
    Route('/crawl', endpoint=run_crawler, methods=['POST'])
]

app = Starlette(routes=routes)
