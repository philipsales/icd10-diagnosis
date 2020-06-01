#!/bin/bash

curl -XPOST 'http://165.22.110.167:9200/2020-icd10-cm/_bulk?pretty' -H "Content-Type: application/x-ndjson" --data-binary "@payload.json" -u elastic 