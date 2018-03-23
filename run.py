#!flask/bin/python
import json
import sys
from firebase import firebase
from flask import Flask, render_template, request, redirect, Response,url_for
import random, json

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('index.html')

@app.route('/receiver', methods = ['POST'])
def signup():
	permit='1'
	data1 = request.json
	if ("@" in data1['email']):
		user= data1['email'].split("@")[0]
		postfix=data1['email'].split("@")[1]
		if len(data1['email'].split("@"))!=2:
			permit='0'
		if postfix!='usc.edu':
			permit='0'
		firebase1 = firebase.FirebaseApplication('https://inf551uscstudent.firebaseio.com', None)
		result = firebase1.get('', None)
		for i in result:
			if str(i)==data1['email'].split("@")[0]:
				permit='0'
				break
		if len(data1['password'])>12 or len(data1['password'])<8:
			permit='0'
	else: permit='0'
	return permit


@app.route('/login', methods = ['POST'])
def signin():
	permit='0'
	data1 = request.json
	if ("@" in data1['email']):
		user= data1['email'].split("@")[0]
		postfix=data1['email'].split("@")[1]		
		firebase1 = firebase.FirebaseApplication('https://inf551uscstudent.firebaseio.com', None)
		result = firebase1.get(user, None)
		if str(result['password'])==str(data1['password']):
			permit=user
		if postfix!='usc.edu':
			permit='0'
		if len(data1['email'].split("@"))!=2:
			permit='0'
	return permit
	#return render_template("search.html", data=permit)


@app.route('/signup')
def redToUp():
	return render_template('signup.html')
@app.route('/signin')
def redToIn():
	return render_template('signin.html')
@app.route('/search')
def redToSe():
	user=request.values.get('user')
	print user
	return render_template('search.html',user=user)

if __name__ == '__main__':
	# run!
	app.run()