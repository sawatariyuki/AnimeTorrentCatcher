# -*- coding: utf-8 -*-
import scrapy

class BangumiTorrentItem(scrapy.Item):
  bangumi = scrapy.Field()
  uploadTime = scrapy.Field()
  sourceType = scrapy.Field()
  aLink = scrapy.Field()
  jimaku = scrapy.Field()
  title = scrapy.Field()
  torrent = scrapy.Field()

class PageUrlItem(scrapy.Item):
  bangumi = scrapy.Field()
  pageUrl = scrapy.Field()