# -* coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, Response, jsonify
import requests, random, json
import sys
from random import *

app = Flask(__name__)

"""
@app.route("/")
def home():
	response = requests.get('http://10.0.1.69:9200')
	json_response = response.json()
	print "\n"
	try:
		print json_response['version']['number']
	except:
		print "Error"
	print "\n"
	name = json_response['cluster_name']
	version = json_response['version']['number']
	return render_template("index.html", name=name, version=version)
	return "Hello World!"
"""

@app.route('/')
def output():
	# serve index template
	return render_template('index.html', name='Joe')

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json()
	print "\n1"
	print data
	print "IP ELASTICSEARCH.: " + data["IP"]
	ip_elasticsearch = data["IP"]
	#print "\n"
	#result = ''
	#if data == None:
	#	data = "ashuashaushaushaush"
	#
	#print "\n2"
	#print data
	#print "\n"

	#data = "ashahsuashuashasua"
	#url = "http://%s:9200/metricbeat-2019.10.09/_search?q=(container.name:*)" % ip_elasticsearch

	#print url
	#response = requests.get(url)
	#json_response = response.json()

	headers = {
    'Content-Type': 'application/json',
	}

	data = '{  "aggs": {    "2": {      "terms": {        "field": "container.image.name.keyword",        "order": {          "_count": "desc"        },        "size": 5      }    }  },  "size": 0,  "_source": {    "excludes": []  },  "stored_fields": [    "*"  ],  "script_fields": {},  "docvalue_fields": [    {      "field": "@timestamp",      "format": "date_time"    },    {      "field": "docker.container.created",      "format": "date_time"    },    {      "field": "system.process.cpu.start_time",      "format": "date_time"    }  ],  "query": {    "bool": {      "must": [        {          "range": {            "@timestamp": {              "format": "strict_date_optional_time",              "gte": "2019-10-08T03:00:00.000Z",              "lte": "2019-10-09T02:59:59.999Z"            }          }        }      ],      "filter": [        {          "match_all": {}        },        {          "match_all": {}        }      ],      "should": [],      "must_not": []    }  }}'
	response = requests.post('http://%s:9200/metricbeat-2019.10.09/_search' % ip_elasticsearch, headers=headers, data=data)

	response_json = response.json()
	buckets = response_json['aggregations']['2']['buckets']
	containers_list = []
	containers_docs = []
	for i in buckets:
		containers_list.append(i["key"])
		containers_docs.append(i["doc_count"])

	print containers_list
	print containers_docs


	

	print "\n"
	#print json_response['hits']['hits'][0]['_source']['@timestamp']
	#response = requests.get('http://%s:9200' % ip_elasticsearch)
	#json_response = response.json()
	print "\n"
	
	response = requests.get('http://%s:9200' % ip_elasticsearch)
	json_response = response.json()
	try:
		print json_response['version']['number']
		print json_response['cluster_name']
		print json_response['tagline']
	except:
		print "Error"
	
	#print "\n"

	name = json_response['cluster_name']
	version = json_response['version']['number']
	message = json_response['tagline']
	#return render_template("index.html", name=name, version=version)

	#data = randint(0,9)

	return jsonify({
		'version': render_template('response.html', version=version),
		'name': render_template('response.html', name=name),
		'message': render_template('response.html', message=message),
		'containers_list': render_template('response.html', containers_list=containers_list),
		'containers_docs': render_template('response.html', containers_docs=containers_docs)
	})

	"""for item in data:
		# loop over every row
		result += str(item['make']) + '\n'

	return result"""


#@app.route("/")
#def home():
#	return render_template("index.html")

if __name__ == "__main__":
	app.run("0.0.0.0", "80", debug=True)