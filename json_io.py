# -* coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, Response, jsonify
import requests, random, json
import sys
from random import *

app = Flask(__name__)


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

	headers = {
    'Content-Type': 'application/json',
	}

	data = '{\
	"aggs":{\
		"2":{\
			"terms":{\
				"field":"container.name.keyword",\
				"order":{\
					"_count":"desc"\
				},"size":20\
			}\
		}\
	},"size":0,"_source":{\
		"excludes":[]\
	},"stored_fields":["*"],\
	"script_fields":{},\
	"docvalue_fields":[{\
		"field":"@timestamp",\
		"format":"date_time"\
	},{\
		"field":"docker.container.created",\
		"format":"date_time"\
	},{\
		"field":"system.process.cpu.start_time",\
		"format":"date_time"\
	}],"query":{\
		"bool":{\
			"must":[{\
				"range":{\
					"@timestamp":{\
						"format":"strict_date_optional_time",\
						"gte":"2019-10-14T20:55:00.000Z",\
						"lte":"2019-10-14T23:59:59.999Z"\
					}\
				}\
			}],"filter":[{\
				"match_all":{}\
			},{\
				"match_all":{}\
			}],"should":[],"must_not":[]\
			}\
		}\
	}'

	data2 = '{"query": {"bool": {"must": [{"range": {"@timestamp": {"gte": "now-15s", "lte": "now"}}},{"query_string": {"query": "docker.memory.usage.pct: *"}}]}}}'
	try:
		response2 = requests.post('http://%s:9200/metricbeat-2019.10.15/_search' % ip_elasticsearch, headers=headers, data=data2)
		response2_json = response2.json()
		print "\n\nJSON 2"
		#print response2_json
		search_size = response2_json['hits']['total']['value']
		print search_size
		print "#########################\n"
	except:
		print "Nada feito! hehe'"

	data2 = '{"size": %s, "query": {"bool": {"must": [{"range": {"@timestamp": {"gte": "now-15s", "lte": "now"}}},{"query_string": {"query": "docker.memory.usage.pct: *"}}]}}}' % search_size
	try:
		response2 = requests.post('http://%s:9200/metricbeat-2019.10.15/_search' % ip_elasticsearch, headers=headers, data=data2)
		response2_json = response2.json()
		print "\n\nJSON 2"
		#print response2_json
		#print response2_json['hits']['hits'][0]["_source"]["container"]["name"]
		#print response2_json['hits']['hits'][0]["_source"]["docker"]["memory"]["usage"]["pct"]
		memory_list = response2_json['hits']['hits']
		print "#########################\n"
	except:
		print "Nada feito! hehe'"

	containers_list_name = []
	containers_memory_usage = []
	for i in memory_list:
		containers_list_name.append(i["_source"]["container"]["name"])
		convert_pct = float(i["_source"]["docker"]["memory"]["usage"]["pct"]) * 100
		print i["_source"]["docker"]["memory"]["usage"]["pct"]
		print convert_pct
		containers_memory_usage.append("%.2f" % convert_pct)

	#for i in containers_memory_usage:
	#	print i
	#for i in containers_list_name:
	#	print i

	response = requests.post('http://%s:9200/metricbeat-2019.10.14/_search' % ip_elasticsearch, headers=headers, data=data)

	response_json = response.json()
	#print response_json
	buckets = response_json['aggregations']['2']['buckets']
	containers_list = []
	containers_docs = []
	for i in buckets:
		containers_list.append(i["key"])
		containers_docs.append(i["doc_count"])

	response = requests.get('http://%s:9200' % ip_elasticsearch)
	json_response = response.json()
	
	name = json_response['cluster_name']
	version = json_response['version']['number']
	message = json_response['tagline']

	return jsonify({
		'version': render_template('response.html', version=version),
		'name': render_template('response.html', name=name),
		'message': render_template('response.html', message=message),
		'containers_list': render_template('response.html', containers_list=containers_list),
		'containers_docs': render_template('response.html', containers_docs=containers_docs),
		'containers_list_name': render_template('response.html', containers_list_name=containers_list_name),
		'containers_memory_usage': render_template('response.html', containers_memory_usage=containers_memory_usage)
	})

if __name__ == "__main__":
	app.run("0.0.0.0", "80", debug=True)