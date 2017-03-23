import requests,pprint,datetime,time,json,os,itertools

#import the current user's public decks, decode the json, and store in setsrequestjson
setsrequest = requests.get('https://api.quizlet.com/2.0/users/wuzza_face/sets/?client_id=pyjFb2bnBN')
setsrequestjson = setsrequest.json()

#dates each deck was created converted from epoch time to a date object
#the day of the week as a numerical value (1-7:Mon-Sun) that corresponds with each date object for decks
days = ([datetime.date.isoweekday(datetime.date.fromtimestamp(item["created_date"])) for item in setsrequestjson])
#print("dates", dates)

#ids of all of the decks that were imported
ids = ([item["id"]for item in setsrequestjson])	


#if history storage is empty, store all id's with numerical day of the week, and a laststudied value of "first study"
if os.stat("testdata.json").st_size == 0:
  newhistory = [{'id': idnum, 'laststudied': freq, 'dayofweek': day} for idnum, freq, day in zip(ids,itertools.repeat('firststudy'),days)]
  print(newhistory)
  with open('testdata.json', 'w') as f:
    json.dump(newhistory,f)


#Open history storage file and load the json into history1
with open('testdata.json', "r") as f:
  historystorage = json.load(f)
#print("historystorage ==" + str(historystorage))
historyids = ([item["id"]for item in historystorage])	
#check if any new sets have been added since the last history store. Add any new sets to the history store with a laststudied value of "first study"
for set in setsrequestjson:
  if set["id"] not in historyids:
    historystorage.append({'id': set["id"],'laststudied': 'firststudy','dayofweek': datetime.date.isoweekday(datetime.date.fromtimestamp(set["created_date"]))}) 
    print(set, " has been added")

'''
#Data needed for printing out the title and date created to user
titledateurl=([{'title':item["title"],'datecreated':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(item["created_date"])),"url":item["url"]}  for item in setsrequestjson])
with open('titledateurl.json', 'w') as f:
	json.dump(titledateurl,f)
print("titledateurl",titledateurl)
###print(type(titledateurl))
###print(titledateurl)
'''


#Create an updated list of days for study based on history storage data
newstudydays = historystorage
print(newstudydays)


for studyday in newstudydays:
  #first study day
  if studyday["laststudied"] == "firststudy" and studyday["dayofweek"] < 7:
    studyday["dayofweek"] += 1
  if studyday["dayofweek"] == 7:
    studyday["dayofweek"] = 1
  #second study day
  if studyday["laststudied"] == "secondstudy":
    if studyday["laststudied"] < 4:
      studyday["dayofweek"] = item["laststudied"] + 3
    elif studyday["dayofweek"] == 5:
      studyday["dayofweek"] = 1
    elif studyday["dayofweek"] == 6:
      studyday["dayofweek"] = 2
    elif studyday["dayofweek"] == 7:
      studyday["dayofweek"] = 3
  #third study day or beyond
  if studyday["laststudied"] == "weeklystudy":
    studyday["dayofweek"] = studyday["dayofweek"]

print("updated",newstudydays)

#calculate what the current day of the week is
currentweekday = datetime.date.isoweekday((datetime.datetime.utcnow()))
print("current day",currentweekday)

for item in newstudydays:
  if item["dayofweek"] == currentweekday:
    print([{request["title"],request["url"],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(request["created_date"]))} for request in setsrequestjson if request["id"] == item["id"]])

studyday = {1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday",7:"Sunday"}
#studyschedule = [studyday.get(day) for day in newstudydays]
#print(studyschedule)
