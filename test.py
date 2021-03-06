import os
from pprint import pprint
from datetime import datetime

from flask import Flask, jsonify, send_from_directory, request
from flask.helpers import safe_join


app = Flask(__name__)
static = os.path.dirname(__file__)


from elasticsearch import Elasticsearch
es = Elasticsearch()
index_name = "test_ac_idx"

def load_dict():
    with open('../english-words/words_alpha.txt') as f:
        return set(f.read().split())

def create_index(es: Elasticsearch, index_name:str):
    response = es.indices.create(
        index=index_name,
        body={
            "mappings": {
                "properties": {
                    "suggest": {
                        "type": "completion"
                    },
                    "title": {
                        "type": "keyword"
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


def fill_data(es:Elasticsearch, index_name:str):
    #res = es.index(index=index_name, id=1, document={ "suggest" : { "input":  "vasya", "weight" : 10 }})
    #res = es.index(index=index_name, id=2, document={ "suggest" : { "input":  "Vanya", "weight": 10 }})
    #res = es.index(index=index_name, id=3, document={ "suggest" : { "input":  "Veronica", "weight": 10 }})
    #res = es.index(index=index_name, id=4, document={ "suggest" : { "input":  "Vader", "weight": 10 }})
    #res = es.index(index=index_name, id=5, document={ "suggest" : { "input":  "Nicolas", "weight": 10 }})
    #res = es.index(index=index_name, id=6, document={ "suggest" : { "input":  "Micolas", "weight": 10 }})

    d = load_dict()
    for id, word in enumerate(d):
        es.index(index=index_name, id=(id+1), document={ "suggest" : { "input":  word, "weight": 10 }})


def es_search(es: Elasticsearch, index_name:str, word:str):
    res = es.search(index=index_name, doc_type='entity',body={
        "suggest": {
            "word-suggest": {
            "prefix": word,
            "completion": {
                "field": "suggest",
                "fuzzy": {
                        "fuzziness": 2
                }
            }
            }
        }
    })
    pprint(res)
    return [item['text'] for item in res['suggest']['word-suggest'][0]['options']]


@app.route('/search')
def search():
    term = request.args.get('term')
    r = es_search(es, index_name, term)
    return jsonify(r)

@app.route('/')
def test():
    return send_from_directory(static, 'autocomplete.html')


if __name__ == '__main__':

    #create_index(es, index_name)
    #fill_data(es, index_name)
    #r = es_search(es, index_name, "xyz")
    #pprint(r)

    app.run()
