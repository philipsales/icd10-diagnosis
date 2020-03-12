icd10_mapping = {
    "settings": {
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
    },
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

}