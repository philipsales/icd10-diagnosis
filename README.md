# icd10-diagnosis
ICD-10 web scraper


# RUNNING CONSOLE APP

## Run the code and save to json
```sh
scrapy runspider icd10.py -o data.json
```

# DEVELOPMENT 

## Run the scrapy shell to explore html structure
```sh
scrapy shell http://<base_url>
response.text
print(response.text)
```
## If response in JSON
```
import json
data = json.loads(resopnse.text)
data.keys()
data['key'][0]
```