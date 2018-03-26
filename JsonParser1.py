import json

data = json.load(open('USC_Schedule1.json'))
USC_Schedule=[]
i=1;
while i<len(data):
	for j in data[i]:
		eachCourse={}
		eachCourse['courseID']=j['courseID']
		eachCourse['courseInstructors']=j['courseInstructors']
		eachCourse['courseName']=j['courseName']
		USC_Schedule.append(eachCourse)
		print eachCourse
	i+=2
f=open('USC_Schedule2.json','w')
f.truncate()
schoolInfo=json.dumps(USC_Schedule)
f.write(schoolInfo)
f.close()
print 'Parsing and writing complete!\n'