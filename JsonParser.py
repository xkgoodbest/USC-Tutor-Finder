import json

data = json.load(open('USC_Schedule.json'))
USC_Schedule=[]
for schoolName_ in data:
	school={}
	school['schoolName']=schoolName_[0]['schoolName']
	USC_Schedule.append(school)
	
	courses=[]
	for dept_ in schoolName_[1]:
		for course_ in dept_[1]:
			for eachSection_ in course_[1]:
				eachCourse_={}
				eachCourse_['courseID']=course_[0]['courseID']
				eachCourse_['courseName']=course_[0]['courseName']
				instructors=''
				for i in eachSection_['courseInstructors']:
					instructors=instructors+i
				eachCourse_['courseInstructors']=instructors
				courses.append(eachCourse_)
	USC_Schedule.append(courses)
i=1
while i < len(USC_Schedule):
	seen = set()
	new_l = []
	for d in USC_Schedule[i]:
		t = tuple(d.items())
		if t not in seen:
			seen.add(t)
			new_l.append(d)
	USC_Schedule[i]=new_l
	i+=2
#print USC_Schedule
f=open('USC_Schedule1.json','w')
f.truncate()
schoolInfo=json.dumps(USC_Schedule)
f.write(schoolInfo)
f.close()
print 'Parsing and writing complete!\n'