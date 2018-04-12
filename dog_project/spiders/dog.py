import scrapy

from dog_project.items import DogInfoItem


class DogInfoSpider(scrapy.Spider):

    name = 'dog_info'

    start_urls = ['http://www.goupuzi.com/thread-htm-fid-4.html']



    def parse(self, response):
        for li in response.css('.breed_content li'):
            # 狗狗名称
            dog_name = li.css('.breed_dogs_name::text').extract()[0]
            ch_name = dog_name[0 : dog_name.find('（')].strip()
            en_name = dog_name[dog_name.find('（') + 1 : dog_name.find('）')].strip()
            # 狗狗指导价
            guide_price = li.css('.breed_dogs_guida::text').extract()[0].replace('指导价：', '').strip()
            # 狗狗头像地址
            avatar = li.css('.breed_conzara_l img::attr(src)').extract()[0]
            dog_info_item = DogInfoItem()
            dog_info_item['name'] = ch_name
            dog_info_item['name_en'] = en_name
            dog_info_item['guide_price'] = guide_price
            dog_info_item['avatar'] = avatar
            # yield dog_info_item
            # 狗狗介绍
            introduce = li.css('.breed_dogs_ency a')[2].css('::attr(href)').extract()[0]
            print(introduce)
            yield scrapy.Request(introduce, self.parse_introduction)

    def parse_introduction(self, response):


        print(response.css('.quanjieshao1 h2::text').extract())


        pass

