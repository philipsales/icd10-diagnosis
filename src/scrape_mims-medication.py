# -*- coding: utf-8 -*-
import scrapy
import copy
import re
import pandas as pd
import json
import time


class Icd10Spider(scrapy.Spider):
    name = 'medication'
    allowed_domains = ['mims.com','sso.mims.com', 'www.mims.com']
    #base_url = 'https://www.mims.com/' # with synyms
    #base_url = 'http://www.mims.com/philippines/browse/alphabet/all?cat=drug&tab=brand'
    #login_url = 'https://sso.mims.com/Account/Signin'
    login_url = "https://sso.mims.com/Account/SignIn?ReturnUrl=%2fAuthentication%2fSendAssertion%3freturnURL%3dhttp%253A%252F%252Fwww.mims.com%252Fphilippines%252FSsoMembership%252FLogOn%253FReturnUrl%253Dhttp%25253A%25252F%25252Fwww.mims.com%25253A80%25252Fphilippines%25252Fbrowse%25252Falphabet%25252Fa%25253Fcat%25253Ddrug%2526dnoa.userSuppliedIdentifier%253Dhttps%25253A%25252F%25252Fsso.mims.com%25252F%2526dnoa.return_to_sig_handle%253DVb_K%2526dnoa.return_to_sig%253DEiTAHW3P8IqK5Y9FJFCyMX4GRuE1Vr7xb6tefeZD2r4%25253D&returnURL=http%3A%2F%2Fwww.mims.com%2Fphilippines%2FSsoMembership%2FLogOn%3FReturnUrl%3Dhttp%253A%252F%252Fwww.mims.com%253A80%252Fphilippines%252Fbrowse%252Falphabet%252Fa%253Fcat%253Ddrug%26dnoa.userSuppliedIdentifier%3Dhttps%253A%252F%252Fsso.mims.com%252F%26dnoa.return_to_sig_handle%3DVb_K%26dnoa.return_to_sig%3DEiTAHW3P8IqK5Y9FJFCyMX4GRuE1Vr7xb6tefeZD2r4%253D"
    start_urls = [login_url] 

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': f"./dataset/missing-requested-data.json"
    }

    def parse(self, response):
        print('RESPONSE URL:', response.url)
        session_id = response.css('input[name="SessionId"]::attr(value)').extract_first()

        data = {
            'EmailAddress': 'peejayaccts@gmail.com',
            'Password': 'UpItDc@2012',
            'RememberMe': 'true',
            'RememberMe': 'false',
            'SessionId': session_id,
            'SubscriberId': '',
            'LicenseNumber': '',
            'CountryCode': 'SG'
        }
        print('session_id: ', session_id)

        #yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.after_login)
        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.after_login)
        #yield scrapy.FormRequest(url=self.base_url, formdata=data, callback=self.after_login)


    def after_login(self, response):
        time.sleep(3)
        base_url = 'http://www.mims.com/philippines/browse/alphabet/a?cat=drug'
        pagelist = ['&tab=brand&page=2', '&tab=brand&page=3']
        for page in pagelist:
            yield scrapy.Request(url=base_url + page, callback=self.action,
                                meta={ 'handle_httpstatus_list': [302], })
                            #meta = { 'dont_redirect': True, 'handle_httpstatus_list': [302] },
    
    def action(self, response):
        time.sleep(3)
        print(response.xpath("//title").get())
        print(response.text)


    '''
    def after_login(self, response):
        print('---AFTER LOGIN----')
        base_url = 'http://mims.com/philippines/browse/alphabet/a?cat=drug'
        pagelist = ['&tab=brand&page=2', '&tab=brand&page=3']
        for page in pagelist:
            yield scrapy.Request(url=base_url + page, callback=self.action)
                            #meta = { 'dont_redirect': True, 'handle_httpstatus_list': [302] },

    def action(self, response):
        print('---PARSE MEDS----')
        pageurl = str(response.url)
        print(pageurl)
        time.sleep(4)
        a_selectors = response.xpath("//title").get()
        #print(response.text)

    '''

    '''
    def after_login(self, response):

        print('print response: ',response.text)
        status = json.loads(response.text)

        if status['IsSuccessful']:
            yield scrapy.Request(url=self.base_url,
                                meta = { 'dont_redirect': True, 'handle_httpstatus_list': [302] },
                                callback=self.parse_meds)

    def parse_meds(self, response):
            #full_xpath
            #/html/body/div[2]/div[10]/div[2]/div[1]/table[2]/tbody/tr[3]/td[2]/a
            #selector
            #content > table:nth-child(6) > tbody > tr:nth-child(3) > td:nth-child(2) > a
            #content > table:nth-child(6) > tbody > tr:nth-child(3) > td:nth-child(2) > a
            urls = response.xpath('#content > table:nth-child(6) > tbody > tr:nth-child(3) > td:nth-child(2) > a::attr(href)').extract()
            print('url:', urls)
        
    '''