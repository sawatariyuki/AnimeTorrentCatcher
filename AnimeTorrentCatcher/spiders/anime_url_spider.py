# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from AnimeTorrentCatcher.items import PageUrlItem
from scrapy.http import Request

class AnimeUrlSpider(scrapy.spiders.Spider):
  base_domain_url = 'https://share.dmhy.org'
  urls = list()
  name = 'AnimeUrlSpider'
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
    bangumiName = urllib.parse.unquote(response.url).split("keyword=")[1]
    item = PageUrlItem()
    item['bangumi'] = bangumiName
    item['pageUrl'] = response.url
    yield item

    urlList = response.xpath('//div[@class="nav_title"]/a[re:test(text(), "下一頁")]/@href').extract()
    if len(urlList) > 0:
      yield Request(url=self.base_domain_url+urlList[0], callback=self.parse)