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

DATASET = 'dataset/diagnosis/icd10-clinical_modification/missing-requested-data.json'
ENVIRONMENT = 'test' 

if ENVIRONMENT == 'prod':
    index_name = '2020-icd10-cm'
    es = Elasticsearch( 
        ['https://157.245.194.218:9200'],
        use_ssl=True,
        verify_certs=False,
        http_auth = ('elastic', 'm3dch3ck@2020_elastic_p@$$'),
        scheme = 'https',
        timeout = int(conn['TIMEOUT']))

elif ENVIRONMENT == 'dev':
    index_name = 'dev.2020-icd10-cm'
    es = Elasticsearch( 
        ['https://157.245.194.218:9200'],
        use_ssl=True,
        verify_certs=False,
        http_auth = ('elastic', 'm3dch3ck@2020_elastic_p@$$'),
        scheme = 'https',
        timeout = int(conn['TIMEOUT']))
elif ENVIRONMENT == 'test':
    index_name = 'test.2020-icd10-cm'
    es = Elasticsearch( 
        ['165.22.110.167'],
        scheme = conn['SCHEME'],
        port = conn['PORT'],
        timeout = int(conn['TIMEOUT']))

def generate_diagnosis():

    try:
        with open(DATASET) as json_file:
            for diagnosis in json.load(json_file):
                _es_id = uuid.uuid4() 
                logger.info(_es_id)
                yield _es_id, diagnosis 

    except Exception as err:
        logger.error(err)

def es_bulk_insert():

    item = ({
            "_index": index_name,
            "_id"   : es_id,
            "_source": diagnosis,
         } for es_id, diagnosis in generate_diagnosis())

    helpers.bulk(es, item)

def _create_mappings():
    mapping = icd10_diagnosis.icd10_mapping

    body =  json.dumps(mapping) 
    main_index =  index_name

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
    _create_mappings()
    es_bulk_insert()


if __name__ == '__main__':
    main()