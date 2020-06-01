GET _search
{
  "query": {
    "match_all": {}
  }
}

#PROD
DELETE /2020-icd10-cm/_doc/cb979c2e-ee02-44b2-ae9a-20e891585235
#secondary diabetes: cb979c2e-ee02-44b2-ae9a-20e891585235

#DEV
DELETE /dev.2020-icd10-cm/_doc/cb979c2e-ee02-44b2-ae9a-20e891585235
#secondary diabetes: cb979c2e-ee02-44b2-ae9a-20e891585235

GET 2020-icd10-cm/_search
{
  "query": {
      "match": {
          "diagnosis": {
              "query" : "NSCLC"
          }
      }
  }
}

GET 2020-icd10-cm/_search
{
    "query": {
        "match_phrase_prefix": {
            "diagnosis.search_analyzer": {
                "query": "hypertension"
            }
        }
    }
}

GET dev.2020-icd10-cm/_search
{
    "query": {
        "multi_match": {
            "query": "secondary diabetes",
            "fields": ["diagnosis","code"]
        }
    }
}

GET 2020-icd10-cm/_search
{
	"query": {
		"match": {
			"diagnosis": {
				"query": "Malignant neoplasm of upper-outer quadrant, left female breast"
			}
		}
	}
}

POST _reindex
{
  "source": {
    "index": "2020-icd10-cm"
  },
  "dest": {
    "index": "bak.2020-icd10-cm"
  }
}


PUT bak.2020-icd10-cm
{
  "mappings": {
      "properties": {
          "type": {
              "type": "keyword"
          },
          "code": {
              "type": "keyword"
          },
          "diagnosis": {
              "type": "text",
              "fields": {
                  "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                  },
                  "simple": {
                      "type": "text",
                      "analyzer": "simple"
                  },
                  "english": {
                      "type": "text",
                      "analyzer": "english"
                  },
                  "autocomplete": {
                      "type": "text",
                      "analyzer": "autocomplete"
                  },
                  "search_analyzer": {
                      "type": "text",
                      "analyzer": "autocomplete_search"
                  }
              }
          },
          "url": {
              "type": "text",
              "fields": {
                  "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                  }
              }
          }
      }
  },
  "settings": {
      "index": {
          "number_of_shards": 2,
          "number_of_replicas": 1
      },
      "analysis": {
          "analyzer": {
              "autocomplete": {
                  "tokenizer": "autocomplete",
                  "filter": [
                      "lowercase"
                      ]
              },
              "autocomplete_search": {
                  "tokenizer": "lowercase"
              }
          },
          "tokenizer": {
              "autocomplete": {
                  "type": "edge_ngram",
                  "min_gram": 3,
                  "max_gram": 10,
                  "token_chars": [
                      "letter" ,
                      "whitespace",
                      "punctuation",
                      "symbol",
                      "digit"
                  ]
              }
          }
      }
  }
}