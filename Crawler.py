import requests
import json
from lxml import etree
URL="https://classes.usc.edu/term-20181/"
htmlPage = requests.get(url = URL)
selector = etree.HTML(htmlPage.content)
allInfo=[]
schoolNames=selector.xpath('//li[@data-type="school"]/a/text()')
schools=selector.xpath('//li[@data-type="school"]/@data-school')
schoolCounter=0
for schoolName_,school_ in zip(schoolNames,schools):
	allInfo.append([])
	allInfo[schoolCounter].append({})
	allInfo[schoolCounter][0]['schoolName']=schoolName_.strip()
	deptNames=selector.xpath('//li[@data-type="department" and @data-school="'+school_+'"]/@data-title')
	deptAbbvs=selector.xpath('//li[@data-type="department" and @data-school="'+school_+'"]/@data-code')
	deptURLs=selector.xpath('//li[@data-type="department" and @data-school="'+school_+'"]/a/@href')
	allInfo[schoolCounter].append([])
	DeptCounter=0
	for deptName_,deptAbbv_,deptURL_ in zip(deptNames,deptAbbvs,deptURLs):
		allInfo[schoolCounter][1].append([])
		allInfo[schoolCounter][1][DeptCounter].append({})
		allInfo[schoolCounter][1][DeptCounter][0]['deptName']=deptName_
		allInfo[schoolCounter][1][DeptCounter][0]['deptAbbv']=deptAbbv_
		allInfo[schoolCounter][1][DeptCounter][0]['deptURL']=deptURL_
		
		allInfo[schoolCounter][1][DeptCounter].append([])
		courseCounter=0
		subHtmlPage = requests.get(url = deptURL_)
		subSelector = etree.HTML(subHtmlPage.content)
		courseIDs=subSelector.xpath('//div[@class="course-info expanded" or @class="course-info expandable"]/@id')
		for courseID_ in courseIDs:
			allInfo[schoolCounter][1][DeptCounter][1].append([])
			allInfo[schoolCounter][1][DeptCounter][1][courseCounter].append({})
			courseName_= subSelector.xpath('//div[@id=\"'+courseID_+'\"]/div/h3/a/text()')
			allInfo[schoolCounter][1][DeptCounter][1][courseCounter][0]['courseName']=courseName_[0].strip()
			allInfo[schoolCounter][1][DeptCounter][1][courseCounter][0]['courseID']=courseID_
			allInfo[schoolCounter][1][DeptCounter][1][courseCounter].append([])
			sectionCounter=0
			courseSections=subSelector.xpath('//div[@id=\"'+courseID_+'\"]//div//tr[contains(.,"Lecture")]/td[@class="section"]/text()')
			for courseSection_ in courseSections:
				courseTime_=subSelector.xpath('//tr[td=\"'+courseSection_+'\"]/td[@class="time"]/text()')
				courseDays_=subSelector.xpath('//tr[td=\"'+courseSection_+'\"]/td[@class="days"]/text()')
				courseInstructors1_=subSelector.xpath('//tr[td=\"'+courseSection_+'\"]/td[@class="instructor"]/a/text()')
				courseInstructors2_=subSelector.xpath('//tr[td=\"'+courseSection_+'\"]/td[@class="instructor"]/text()')
				allInfo[schoolCounter][1][DeptCounter][1][courseCounter][1].append({})
				allInfo[schoolCounter][1][DeptCounter][1][courseCounter][1][sectionCounter]['courseSection']=courseSection_
				if len(courseTime_)>0: allInfo[schoolCounter][1][DeptCounter][1][courseCounter][1][sectionCounter]['courseTime']=courseTime_[0]
				if len(courseDays_)>0: allInfo[schoolCounter][1][DeptCounter][1][courseCounter][1][sectionCounter]['courseDays']=courseDays_[0]
				allInfo[schoolCounter][1][DeptCounter][1][courseCounter][1][sectionCounter]['courseInstructors']=courseInstructors1_+courseInstructors2_
				sectionCounter+=1
			courseCounter+=1
		print 'Processed',deptAbbv_,',',schoolName_.strip()
		DeptCounter+=1
	schoolCounter+=1
print '\n\nAll Info processed, parsing and writing!\n'

f=open('USC_Schedule.json','w')
f.truncate()
schoolInfo=json.dumps(allInfo)
f.write(schoolInfo)
f.close()
print 'Parsing and writing complete!\n'