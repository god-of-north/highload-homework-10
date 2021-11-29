from pprint import pprint
from datetime import datetime

from elasticsearch import Elasticsearch
es = Elasticsearch()

def load_dict():
    with open('../english-words/words_alpha.txt') as f:
        return set(f.read().split())

def create_index(es: Elasticsearch, index_name:str):
    response = es.indices.create(
        index=index_name,
        body={
            "settings": {
                "analysis": {
                    "filter": {
                        "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": 1,
                        "max_gram": 10
                        }
                    },
                    "analyzer": {
                        "autocomplete": { 
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "autocomplete_filter"
                        ]
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "autocomplete", 
                        "search_analyzer": "standard"
                    }
                }
            }
        },
        ignore=400 # ignore 400 already exists code
    )

    print ('response:', response)
    if 'acknowledged' in response and response['acknowledged'] == True:
        print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
        return True
    elif 'error' in response:
        print ("ERROR:", response['error']['root_cause'])
        print ("TYPE:", response['error']['type'])

    return False

index_name = "test_ac_idx"
#create_index(es, index_name)
#
#res = es.index(index=index_name, id=1, document={"title":"Vasya"})
#if 'result' in response and response['result'] == 'created':
#    return True
#print(res)
#res = es.index(index=index_name, id=2, document={"title":"Vanya"})
#res = es.index(index=index_name, id=3, document={"title":"Veronica"})
#res = es.index(index=index_name, id=4, document={"title":"Vader"})
#res = es.index(index=index_name, id=5, document={"title":"Nicolas"})
#res = es.index(index=index_name, id=6, document={"title":"Micolas"})

#d = load_dict()
#for id, word in enumerate(d):
#    res = es.index(index=index_name, id=id, document=word)

#res = es.get(index=index_name, id=1)
#print(res, '\n', res['_source'])

#es.indices.refresh(index=index_name)

#res = es.search(index=index_name, query={"match_all": {}})
#pprint(res)
#print("Got %d Hits:" % res['hits']['total']['value'])
#for hit in res['hits']['hits']:
#    print("%(title)s" % hit["_source"])


res = es.search(index=index_name, query={
        "bool": {
            "should": [
                {
                    "prefix": {
                        "title": "va"
                    }
                }
            ]
        }
    })

print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(title)s" % hit["_source"])