# -*- coding: utf-8 -*-
import scrapy
import copy
import re
import pandas as pd


class Icd10Spider(scrapy.Spider):
    name = 'icd10'
    allowed_domains = ['icd10data.com']
    start_urls = ['https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00']

    def parse(self, response):
        self.log('Url: ' + response.url)

        icd10_code = ''
        icd10_diagnosis = ''
        icd10_synonyms = ''

        icd10_code = response.css('span.identifierDetail::text').extract_first(),
        icd10_diagnosis = response.css('h2.codeDescription::text').extract_first(),
        icd10_synonyms = response.xpath('//span[contains(text(),"Approximate Synonyms")]/following-sibling::ul').get().strip()
        icd10_applicables = response.xpath('//span[contains(text(),"Applicable To")]/following-sibling::ul').get()

        yield self._set_standard_diagnosis(icd10_code, icd10_diagnosis)
        yield self._set_nonstandard_diagnosis(icd10_code, icd10_synonyms)


    def _set_standard_diagnosis(self, icd10_code, icd10_diagnosis):
        
        standard_diagnosis = {
            'type': 'standard', 
            'code': icd10_code[0],
            'diagnosis': icd10_diagnosis[0]
        }

        yield standard_diagnosis

    def _set_nonstandard_diagnosis(self, icd10_code, diagnosis_list):
        syn_list = []
        if diagnosis_list::

            sp = StringProcessor(icd10_synonyms)
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
