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

es = Elasticsearch( 
    nodes,
    http_auth = (conn['USERNAME'], conn['PASSWORD']),
    scheme = conn['SCHEME'],
    port = conn['PORT'],
    timeout = int(conn['TIMEOUT']))

def set_json_dump():
    _create_mappings()
    counter = 0
    bulk_data = []

    data = [
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Cancer metastatic to lung"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Cancer metastatic to lung undifferentiated lg cell"}
    ]

    docs = json.dumps(data)

    logger.info(docs)
    """
    for doc in docs:
        try:
            index = '2022-icd10-cm'

            _header = { 
                "create" : { 
                    "_index" : index,  
                    "_type" : '_doc', 
                    "_id" : uuid.uuid4() 
                } 
            }

            bulk_data.append(_header)
            #bulk_data.append(json.dumps(_body[0]))
            bulk_data.append(doc)
            counter += 1

        except TypeError:
            logger.error("NoneType object!")
            continue
    logger.info("total index inserts :" + str(len(doc)))
    print(bulk_data)
    """
    
    #_bulk_dump(bulk_data)
def decode_nginx_log():
    _data = [
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Cancer metastatic to lung"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Cancer metastatic to lung undifferentiated lg cell"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Cancer metastatic to lung, adenocarcinoma"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Cancer metastatic to lung, small cell"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Cancer metastatic to lung, squamous cell"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Cancer of the thyroid, with metastasis to lungs"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Melanoma eye, metastatic to lung"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Melanoma eye, metastatic to pancreas"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Melanoma, metastatic to lung"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Metastasis to lung from adenocarcinoma"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Secondary adenocarcinoma of lung"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Secondary malignant melanoma of lung"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Secondary malignant melanoma of lung from eye"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Secondary malignant melanoma of pancreas from eye"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Secondary malignant neoplasm of lung"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Secondary malignant neoplasm of lungs from thyroid"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Secondary small cell cancer of lung"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Secondary squamous cell carcinoma of lung"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Secondary undifferentiated large cell malignant neoplasm of lung"},
        {"type": "synonyms", "code": "C78.00", "url": "https://www.icd10data.com/ICD10CM/Codes/C00-D49/C76-C80/C78-/C78.00", "diagnosis": "Cancer metastatic to lung"}
    ]

    for item in _data:
        _idx = uuid.uuid4() 
        yield _idx, item 

def es_add_bulk():

    k = ({
            "_index": "2021-icd-10-cm",
            "_type" : "icd10",
            "_id"   : idx,
            "_source": item,
         } for idx, item in decode_nginx_log())

    helpers.bulk(es, k)

def _bulk_insert():
    actions = [
        {
            "_index": "tickets-index",
            "_type": "tickets",
            "_id": j,
            "_source": {
                "any":"data" + str(j),
                "timestamp": datetime.now()}
        } for j in range(0, 10)
    ]

    helpers.bulk(es, actions)

def _bulk_dump(bulk_data):

    try:
        es.bulk(bulk_data)  
    except (ConnectionError) as err: 
        logger.error(error)
    except ValueError as e:
        logger.error(e)

def _create_mappings():
    mapping = icd10_diagnosis.icd10_mapping

    body = json.dumps(mapping)
    main_index = '2022-icd10-cm' 

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
    #_bulk_insert()
    es_add_bulk()
    #set_json_dump() 


if __name__ == '__main__':
    main()