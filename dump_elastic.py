import sys 
import uuid
import json
import logging
from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError 
from elasticsearch import helpers

import lib.logs.logging_conf, logging
logger = logging.getLogger("elasticsearch.connection")
import lib.logs.logger as etl_log 

from schema import icd10_diagnosis 

from settings.base_conf import elastic_config
conn = elastic_config.ElasticSearchConfig[elastic_config.ElasticSearchENV]

INDEX = conn['INDEX']
DOC_TYPE = conn['TYPE']
HOST1 = conn['HOST']
HOST2 = conn['HOST']
nodes = [HOST1, HOST2]


#PRODUCTION
es = Elasticsearch( 
    ['https://157.245.194.218:9200'],
    use_ssl=True,
    verify_certs=False,
    http_auth = ('', ''),
    scheme = 'https',
    timeout = int(conn['TIMEOUT']))
'''
#DEVELOPMENT

es = Elasticsearch( 
    ['165.22.110.167'],
    scheme = conn['SCHEME'],
    port = conn['PORT'],
    timeout = int(conn['TIMEOUT']))
'''

def generate_diagnosis():

    try:
        #with open('dataset/new_index/data-170478-new.json') as json_file:
        #with open('dataset/new_index/additional-data.json') as json_file:
        with open('dataset/missing-requested-data.json') as json_file:
            for diagnosis in json.load(json_file):
                _es_id = uuid.uuid4() 
                logger.info(_es_id)
                yield _es_id, diagnosis 

    except Exception as err:
        logger.error(err)

def es_bulk_insert():

    item = ({
            "_index": '2020-icd10-cm',
            #"_index": 'icd10_mapping', 
            "_id"   : es_id,
            "_source": diagnosis,
         } for es_id, diagnosis in generate_diagnosis())

    helpers.bulk(es, item)

def _create_mappings():
    mapping = icd10_diagnosis.icd10_mapping

    #body = '{ "mappings": ' + json.dumps(mapping) + ' }'
    body =  json.dumps(mapping) 
    main_index = 'dev.2020-icd10-cm' 

    if es.indices.exists(main_index):
        logger.debug("INDEX exists")
    else:
        try: 
            res = es.indices.create(index = main_index, body = body )
            logger.info(res)

            if res["acknowledged"] != True:
                logger.info("Index creation failed")
            else:
                logger.info("Index created")

        except ConnectionError as err:
            logger.error(err)

def main():
    #_create_mappings()
    es_bulk_insert()


if __name__ == '__main__':
    main()