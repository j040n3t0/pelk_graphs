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
	#data = request.get_json()
	#print "\n1"
	#print data
	#print "\n"
	#result = ''
	#if data == None:
	#	data = "ashuashaushaushaush"
	#
	#print "\n2"
	#print data
	#print "\n"

	#data = "ashahsuashuashasua"

	response = requests.get('http://10.0.1.69:9200')
	json_response = response.json()
	print "\n"
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
			'message': render_template('response.html', message=message)
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