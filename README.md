# highload-homework-10

Elasticsearch autocomplete

## Installing 

```
git clone https://github.com/god-of-north/highload-homework-10.git
docker-compose build
docker-compose up -d
```

## Elasticsearch index & query

Index mapping:
```
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
```

Search query:
```
"suggest": {
    "word-suggest": {
        "prefix": word,
        "completion": {
            "field": "suggest",
            "fuzzy": {
                "fuzziness": "AUTO:3,7"
            }
        }
    }
}
```

## Testing

When web service is started you can open main window:
http://localhost:5000/

After first input(if the index was not created) elasticserch will create index and start filling it with the data.

Now you can type your text for autocompletion testing.