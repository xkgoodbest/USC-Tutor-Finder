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
	data1 = request.json
	#username=data1['email'].split('@')[0]
	print data1
	return 'data1'

if __name__ == '__main__':
	# run!
	app.run()