import json
import requests

host = 'http://elasticsearch:9200'

# Load from JSON
with open('seed.json') as data_file:    
    data = json.load(data_file)

# Create index 'feed'
requests.put(host + '/feed', data=json.dumps(
	{
		'settings': {
            'index': {
                'number_of_shards': 1,
                'number_of_replicas': 0
            },
            'analysis': {
                'analyzer': {
                    'standard_with_strip_html_tags': {
                        'tokenizer': 'standard',
                        'char_filter': ['html_strip']
                    }
                }
            }
        },
	    'mappings': {
	        'news': {
	            'properties': {
	                'title': { 'type' : 'text', 'analyzer': 'standard' },
	                'body': { 'type' : 'text', 'analyzer': 'standard_with_strip_html_tags' }
	            }
	        }
	    }
	}
))


# Seed data
for item in data:
    news = { 'title': item['title'], 'body': item['body'] }
    requests.put(host + '/feed/news/' + item['id'], data=json.dumps(news))
