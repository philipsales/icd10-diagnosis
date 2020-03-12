
ElasticSearchENV = "local"

ElasticSearchConfig = {
    'local': {
        'USERNAME': '',
        'PASSWORD': '',
        'INDEX': '2019-icd-10-cm',
        'TYPE': '_doc',
        'SCHEME': 'HTTP',
        'HOST': 'localhost',
        'PORT': 9200,
        'TIMEOUT': 3600
    },
    'development': {
        'USERNAME': '',
        'PASSWORD': '',
        'INDEX': 'philippines',
        'TYPE': 'patients',
        'SCHEME': 'https',
        'HOST': 'elk.curis.online',
        'PORT': 9200,
        'TIMEOUT': 360
    },
    'production': {
        'USERNAME': 'elastic',
        'PASSWORD': 'elastic',
        'INDEX': 'philippines',
        'TYPE': 'patients',
        'SCHEME': 'HTTP',
        'HOST': 'localhost',
        'PORT': 9200,
        'TIMEOUT': 360
    }
}





