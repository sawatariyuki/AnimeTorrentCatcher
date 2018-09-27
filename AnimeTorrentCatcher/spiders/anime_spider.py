# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from AnimeTorrentCatcher.items import BangumiTorrentItem
from scrapy.http import Request

class AnimeSpider(scrapy.spiders.Spider):
  base_domain_url = 'https://share.dmhy.org'
  name = 'AnimeSpider'
  allowed_domains = ['share.dmhy.org']
  start_urls = [
    # 'https://share.dmhy.org/topics/list?keyword=%E5%B0%91%E5%A5%B3%E2%98%86%E6%AD%8C%E5%89%A7'
    "https://share.dmhy.org/topics/list?keyword=island",
    "https://share.dmhy.org/topics/list?keyword=工作细胞",
    "https://share.dmhy.org/topics/list?keyword=轻羽飞扬",
    "https://share.dmhy.org/topics/list?keyword=来玩游戏吧",
    "https://share.dmhy.org/topics/list?keyword=音乐少女",
    "https://share.dmhy.org/topics/list?keyword=邪神与厨二病少女",
    "https://share.dmhy.org/topics/list?keyword=One Room 第二季",
    "https://share.dmhy.org/topics/list?keyword=命运石之门 0",
    "https://share.dmhy.org/topics/list?keyword=春原庄的管理人小姐",
    "https://share.dmhy.org/topics/list?keyword=异世界魔王与召唤少女的奴隶魔术",
    "https://share.dmhy.org/topics/list?keyword=某僵尸少女的灾难",
    "https://share.dmhy.org/topics/list?keyword=敦君与女朋友",
    "https://share.dmhy.org/topics/list?keyword=遥的接球",
    "https://share.dmhy.org/topics/list?keyword=杀戮天使",
    "https://share.dmhy.org/topics/list?keyword=昴宿七星",
    "https://share.dmhy.org/topics/list?keyword=少女☆歌剧",
    "https://share.dmhy.org/topics/list?keyword=百炼霸王与圣约女武神",
    "https://share.dmhy.org/topics/list?keyword=暗芝居 第六季",
    "https://share.dmhy.org/topics/list?keyword=Happy Sugar Life",
    "https://share.dmhy.org/topics/list?keyword=摇曳庄的幽奈小姐",
    "https://share.dmhy.org/topics/list?keyword=BanG Dream!",
    "https://share.dmhy.org/topics/list?keyword=偶像大师 灰姑娘女孩剧场 第三季"
  ]

  def parse(self, response):
    bangumiNameList = urllib.parse.unquote(response.url).split("keyword=")
    bangumiName = bangumiNameList[1] if len(bangumiNameList) == 2 else ''
    yield Request(url=response.url, meta={'bangumiName': bangumiName}, callback=self.parse_page)

    urlList = response.xpath('//div[@class="nav_title"]/a[re:test(text(), "下一頁")]/@href').extract()
    if len(urlList) > 0:
      yield Request(url=self.base_domain_url+urlList[0], callback=self.parse)

  def parse_page(self, response):
    bangumiName = response.meta['bangumiName']
    for tr in response.xpath('//tbody/tr'):
      uploadTimeList = tr.xpath('td[re:test(@width, "^\d(\d)+")]/text()').extract()
      uploadTime = uploadTimeList[0].strip() if len(uploadTimeList) > 0 else ''

      sourceTypeList = tr.xpath('td/a//font/text()').extract()
      sourceType = sourceTypeList[0].strip() if len(sourceTypeList) > 0 else ''

      aLinkList = tr.xpath('td[@class="title"]/a/@href').extract()
      aLink = self.base_domain_url + aLinkList[0].strip() if len(aLinkList) > 0 else ''

      jimakuList = tr.xpath('td[@class="title"]/span[@class="tag"]/a/text()').extract()
      jimaku = jimakuList[0].strip() if len(jimakuList) > 0 else ''

      titleList = tr.xpath('string(td[@class="title"]/a)').extract()
      title = titleList[0].strip() if len(titleList) > 0 else ''
      
      item = BangumiTorrentItem()
      item['bangumi'] = bangumiName
      item['uploadTime'] = uploadTime
      item['sourceType'] = sourceType
      item['aLink'] = aLink
      item['jimaku'] = jimaku
      item['title'] = title
      yield Request(url=aLink, meta={'item': item}, callback=self.parse_subPage)

  def parse_subPage(self, response):
    item = response.meta['item']
    torrent = response.xpath('//div[@id="resource-tabs"]//p/a[@id="magnet2"]/@href').extract()[0].strip()
    item['torrent'] = torrent
    yield item