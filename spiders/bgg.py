import scrapy
from scrapy import Request
from ..items import BggItem


class BggSpider(scrapy.Spider):
    name = 'bgg'
    start_urls = ['https://boardgamegeek.com/browse/boardgame/']
    page_count = 1

    def parse(self, response):
        games_list = response.xpath('//div[@id="collection"]//tr[@id="row_"]')

        for index, game in enumerate(games_list):
            item = BggItem()

            item['ranking'] = game.xpath('./td[@class="collection_rank"]//a/@name').get()
            item['name'] = game.xpath(f'./td[@id="CEcell_objectname{index + 1}"]//a/text()').get()
            item['year'] = game.xpath(f'./td[@id="CEcell_objectname{index + 1}"]//span[@class="smallerfont dull"]//text()').get().replace("(", "").replace(")", "")
            item['rating_geek'] = game.xpath('./td[@class="collection_bggrating"][1]//text()').get().strip()
            item['rating_avg'] = game.xpath('./td[@class="collection_bggrating"][2]//text()').get().strip()
            item['num_voters'] = game.xpath('./td[@class="collection_bggrating"][3]//text()').get().strip()

            yield item

        self.page_count += 1

        next_page = f'{self.start_urls[0]}page/{self.page_count}/'
        if next_page:
            yield Request(url=next_page, callback=self.parse)