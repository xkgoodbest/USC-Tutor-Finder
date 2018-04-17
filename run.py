#!flask/bin/python
import json
import sys
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from collections import Counter

from firebase import firebase
from flask import Flask, render_template, request, redirect, Response,url_for, session,jsonify
import random, json
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps

app = Flask(__name__)
app.secret_key = "super secret key"
@app.route('/')
def output():
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
		if result:
			if str(result['password'])==str(data1['password']) :
				permit=user
			if postfix!='usc.edu':
				permit='0'
			if len(data1['email'].split("@"))!=2:
				permit='0'
	if permit !='0':
		session['signin'] = True
		session['username'] = user
	return permit

#sign out		
@app.route('/signout')
def signout():
	session.clear()
	return redirect(url_for('redToIn'))

@app.route('/signup')
def redToUp():
	return render_template('signup.html')
@app.route('/signin')
def redToIn():
	return render_template('signin.html')
@app.route('/search')
def redToSe():
	user=request.values.get('user')
	return render_template('search.html',user=user)
@app.route('/searchItem/<jsdata>', methods = ['GET'])
def searchItems(jsdata):
	firebase1 = firebase.FirebaseApplication('https://inf551uscstudent.firebaseio.com/', None)
	studentData = firebase1.get('', None)
	firebase2 = firebase.FirebaseApplication('https://inf551usc-61ddc.firebaseio.com/', None)
	courseData = firebase2.get('', None)
	subQueries=json.loads(jsdata)['query'].split()[1:]
	option=json.loads(jsdata)['query'].split()[0]
	numbers=[]
	if option=='0':
		for subQuery in subQueries:
			for number,oneCourse in enumerate(courseData):
				if(subQuery.lower() in oneCourse['courseID'].lower()):
					numbers.append(number)
	elif option=='1':
		for subQuery in subQueries:
			for number,oneCourse in enumerate(courseData):
				if(subQuery.lower() in oneCourse['courseInstructors'].lower()):
					numbers.append(number)
	else:
		for subQuery in subQueries:
			for number,oneCourse in enumerate(courseData):
				if(subQuery.lower() in oneCourse['courseName'].lower()):
					numbers.append(number)
	time_counts = Counter(numbers)
	numbers=list(set(numbers))
	top= time_counts.most_common(len(numbers))
	numbers=list(zip(*top)[0])
	returnList=list(courseData[i] for i in numbers )
	for oneCourse in returnList:
		will=[]

		for oneStudent in studentData.keys():
			if studentData[oneStudent].has_key('will'):
				for aCourse in studentData[oneStudent]['will']:
					if aCourse['courseID']==oneCourse['courseID'] and aCourse['instructors']==oneCourse['courseInstructors']:
						will.append(studentData[oneStudent]['email'])
		oneCourse['willToTutor']=will
	return jsonify(returnList)
#profile.html
class ProfileEdit(Form):
	email = StringField("Email", [validators.Length(min = 1, max = 50)])
	name  = StringField("Full Name", [validators.Length(min = 1, max = 30)])
	Cur_Pwd = StringField("Current Password",[validators.Length(min = 8, max = 12)])
	New_pwd1 = StringField("New Password",[validators.Length(min = 8, max = 12)])
	New_pwd2 = StringField("Confirm New Password",[
			validators.DataRequired(),
			validators.EqualTo('New Password', message = 'Passwords do not match')
		])
	Tut_info = StringField("Your Tutor Info")
	Stu_info = StringField("Your Student Info")		

@app.route('/profile', methods=['GET','POST'])
def redToProfile():
	form = ProfileEdit(request.form)
	if request.method == 'POST' and form.validate():
		email = form.email.data
		name = form.name.data
		Cur_Pwd = form.Cur_Pwd.data
		New_pwd1 = form.New_pwd1.data
		New_pwd2 = form.New_pwd1.data

		form = FirePut()
		if form.validate_on_submit():
			putData = {}

		return render_template('profile.html')

	return render_template('profile.html', form=form)
	
@app.route('/reset_pwd')
def rest_pass():
	return render_template('reset_pwd.html')


if __name__ == '__main__':
	# run!
	app.run(debug=True)