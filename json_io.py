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
						"gte":"2019-10-09T20:55:00.000Z",\
						"lte":"2019-10-09T23:59:59.999Z"\
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
	response = requests.post('http://%s:9200/metricbeat-2019.10.09/_search' % ip_elasticsearch, headers=headers, data=data)

	response_json = response.json()
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
		'containers_docs': render_template('response.html', containers_docs=containers_docs)
	})

if __name__ == "__main__":
	app.run("0.0.0.0", "80", debug=True)