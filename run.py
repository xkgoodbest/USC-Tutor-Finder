#!flask/bin/python
import json
import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('index.html', name='Joe!')

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data1 = request.data
	result = ''
	#for item in data1:
	#	result += str(item['make']) + '\n'

	return data1

if __name__ == '__main__':
	# run!
	app.run()