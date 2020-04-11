# -*- coding: utf-8 -*-
import scrapy


class Icd10Spider(scrapy.Spider):
    name = 'icd10'
    allowed_domains = ['icd10.com']
    start_urls = ['http://icd10.com/']

    def parse(self, response):
        pass
