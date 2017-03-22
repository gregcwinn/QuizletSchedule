import requests,pprint,datetime,time,json,os,itertools

#import the current user's public decks, decode the json, and store in setsrequestjson
setsrequest = requests.get('https://api.quizlet.com/2.0/users/wuzza_face/sets/?client_id=pyjFb2bnBN')
setsrequestjson = setsrequest.json()

#Data needed for printing out the title and date created to user
titledateurl=([[item["title"],time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item["created_date"])),item["url"]] for item in setsrequestjson])
with open('titledateurl.json', 'w') as f:
	json.dump(titledateurl,f)

###print(type(titledateurl))
###print(titledateurl)


#dates each deck was created converted from epoch time to a date object
dates = ([datetime.date.fromtimestamp(item["created_date"]) for item in setsrequestjson])
#the day of the week as a numerical value (1-7:Mon-Sun) that corresponds with each date object for decks
days = ([datetime.date.isoweekday(item) for item in dates])

#ids of all of the decks that were imported
id = ([item["id"]for item in setsrequestjson])	

#if history storage is empty, store all id's with numerical day of the week, and a starting study day value of 1
if os.stat("testdata.json").st_size == 0:
	newhistory = list(zip(id,itertools.repeat(1),days))
	print(newhistory)
	with open('testdata.json', 'w') as f:
		json.dump(newhistory,f)

#open history storage file and load the json into history1
with open('testdata.json', 'r') as f:
	historystorage = json.load(f)
print("historystorage ==" + str(historystorage))

#TODO Need to add the day of the week to the list of ids and frequency


"""
num = 0
for set in titledateurl:
	set[1] = days[num]
	num += 1
#test data
datesfrequency = [(1,3),(2,3),(3,3),(1,5),(2,5),(3,5),(1,7),(2,7),(3,7)]
"""

new = []
for item in historystorage:
	#first study day
	if item[1] == 1 and item[2] < 7:
		new.append(item[2] + 1)
		if item[1] == 7:
			new.append(0)	
	#second study day
	if item[1] == 2:
		if item[1] < 4:
			new.append((item[1] + 3))
		elif item[2] == 5:
			new.append(1)
		elif item[2] == 6:
			new.append(2)
		elif item[2] == 7:
			new.append(3)
	#third study day or beyond
	if item[1] == 3:
		new.append(item[2])

print(new)
studyday = {1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday",7:"Sunday"}
studyschedule = [studyday.get(day) for day in new]
print(studyschedule)
num = 0
for set in historystorage:
	set[2] = studyschedule[num]
	num += 1
print(historystorage)

