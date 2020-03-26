# -*- coding: utf-8 -*-
import scrapy
import copy
import re
import pandas as pd


class Icd10Spider(scrapy.Spider):
    name = 'icd10'
    allowed_domains = ['icd10data.com']
    base_url = 'https://www.icd10data.com' # with synyms
    #start_urls = ['https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00'] # with synyms

    '''
    pages = pd.read_csv('links.csv')
    all_pages = pages['pages']
    all_pages.drop_duplicates(keep=False, inplace=True)
    page_links = list(all_pages)
    '''
    pages = pd.read_csv('links/new_links.csv')
    all_pages = pages['pages']
    page_links = list(all_pages)

    #index = 0
    #index = 9937
    #index = 78513
    index = 79312
    #start_urls = [ base_url + page_links[index]]
    #start_urls = ['https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00'] # with synyms
    start_urls = ['https://www.icd10data.com/ICD10CM/Codes/C00-D49/C60-C63/C61-/C61'] #with synonums --> Prostate
    #start_urls = ['https://www.icd10data.com/ICD10CM/Codes/A00-B99/A00-A09/A06-/A06.0'] #without synyms but applicable to

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': f"./dataset/{name}.%(time)s.json"
    }



    def parse(self, response):
        self.log('Url: ' + response.url)

        icd10_code = ''
        icd10_diagnosis = ''
        icd10_synonyms = ''

        icd10_code = response.css('span.identifierDetail::text').extract_first(),
        icd10_diagnosis = response.css('h2.codeDescription::text').extract_first(),
        icd10_synonyms = response.xpath('//span[contains(text(),"Approximate Synonyms")]/following-sibling::ul').get()
        icd10_applicables = response.xpath('//span[contains(text(),"Applicable To")]/following-sibling::ul').get()
        print('-----icd_applicable----',icd10_applicables)
        print('-----icd_synonyms-----',icd10_synonyms)



        if icd10_applicables:
            sp_applicable = StringProcessor(icd10_applicables)
            applicables = sp_applicable.dup().clean_html().split().remove_whitespace()
            print('-----APLICABLE----',applicables)

            for applicable in applicables:
                applicable_diagnosis = {}
                applicable_diagnosis['type'] = 'applicable' 
                applicable_diagnosis['code'] = icd10_code[0]
                applicable_diagnosis['url'] = response.url 
                applicable_diagnosis['diagnosis'] = applicable 
                yield applicable_diagnosis

        #approximate_synomyms
        elif icd10_synonyms:
            sp_synonyms = StringProcessor(icd10_synonyms)
            synonyms = sp_synonyms.dup().clean_html().split().remove_whitespace()
            print('-----SYNONYMS----',synonyms)

            for synonym in synonyms:
                synonym_diagnosis = {}
                synonym_diagnosis['type'] = 'synonyms' 
                synonym_diagnosis['code'] = icd10_code[0]
                synonym_diagnosis['url'] = response.url 
                synonym_diagnosis['diagnosis'] = synonym
                yield synonym_diagnosis


        else:
            diagnosis = {
                'type': 'standard', 
                'code': icd10_code[0],
                'url': response.url,
                'diagnosis': icd10_diagnosis[0]
            }

            yield diagnosis


        #if self.page_links[self.index]:
        '''
        if self.index != len(self.page_links)-1:
            next_link = self.page_links[self.index]
            self.index += 1
            new_url = self.base_url + next_link

            print('------URL------:' + response.url)
            print('------counter------:'+ str(self.index) + ' / ' + str(len(self.page_links)))
            
            yield scrapy.Request(url=new_url, callback=self.parse)
        '''

        
        #yield self._set_nonstandard_diagnosis(icd10_code, icd10_synonyms)
        #yield self._set_nonstandard_diagnosis(icd10_code, icd10_applicables)


    def _set_standard_diagnosis(self, icd10_code, icd10_diagnosis):
        print('------HELLO_-------')
        diagnosis = {
            'type': 'standard', 
            'code': icd10_code[0],
            'diagnosis': icd10_diagnosis[0]
        }
        print(diagnosis)

        yield diagnosis

        

    def _set_nonstandard_diagnosis(self, icd10_code, nonstandard_diagnosis):
        syn_list = []

        if nonstandard_diagnosis:
            sp = StringProcessor(nonstandard_diagnosis)
            synonyms = sp.dup().clean_html().split().remove_whitespace()

            for synonym in synonyms:
                synonym_diagnosis = {}
                synonym_diagnosis['type'] = 'synonyms' 
                synonym_diagnosis['code'] = icd10_code[0]
                synonym_diagnosis['diagnosis'] = synonym
                yield synonym_diagnosis


class StringProcessor(object):
    def __init__(self, st):
        self._st = st

    def dup(self):
        return copy.deepcopy(self)

    def clean_html(self):
        cleanr = re.compile('\r|<.*?>')
        self._st = re.sub(cleanr, '', self._st)
        return self

    def split(self):
        self._st = self._st.split('\n')[1:-1]
        return self
    
    def remove_whitespace(self):
        return [i.lstrip() for i in self._st if i]
