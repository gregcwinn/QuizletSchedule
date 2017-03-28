import requests,pprint,datetime,time,json,os,itertools

class StudySets:

  def __init__(self,setsrequestjson):
    self.setsrequestjson = setsrequestjson

  #dates each deck was created converted from epoch time to a date object
  #the day of the week as a numerical value (1-7:Mon-Sun) that corresponds with each date object for decks
  def epochtodate(self):
    days = ([datetime.date.isoweekday(datetime.date.fromtimestamp(item["created_date"])) for item in self.setsrequestjson])
    return days

  #ids of all of the decks that were imported
  def listofids(self):
    ids = ([item["id"]for item in self.setsrequestjson])	
    return ids

  #if history storage is empty, store all id's with numerical day of the week, and a laststudied value of "first study"
  def ishistoryempty(self,ids,days):
    if os.stat("testdata.json").st_size == 0:
      initialhistorydata = [{'id': idnum, 'laststudied': freq, 'dayofweek': day} for idnum, freq, day in zip(ids,itertools.repeat('firststudy'),days)]
      with open('testdata.json', 'w') as f:
        json.dump(initialhistorydata,f)

  #open history storage file and load the json into history1
  def gethistory(self):
    with open('testdata.json', "r") as f:
      historystorage = json.load(f)
    return historystorage

  #check if any new sets have been added since the last history store. Add any new sets to the history store with a laststudied value of "first study"
  def addnewsets(self,historystorage):
    historyids = ([item["id"]for item in historystorage])	
    for set in self.setsrequestjson:
      if set["id"] not in historyids:
        historystorage.append({'id': set["id"],'laststudied': 'firststudy','dayofweek': datetime.date.isoweekday(datetime.date.fromtimestamp(set["created_date"]))}) 


  #Create an updated list of days for study based on history storage data
  def nextstudydays(self,historystorage):
    newstudydays = historystorage
    for studyday in newstudydays:
      #first study day
      if studyday["laststudied"] == "firststudy" and studyday["dayofweek"] < 7:
        studyday["dayofweek"] += 1
      if studyday["dayofweek"] == 7:
        studyday["dayofweek"] = 1
      #second study day
      if studyday["laststudied"] == "secondstudy":
        if studyday["dayofweek"] < 4:
          studyday["dayofweek"] = studyday["dayofweek"] + 3
        elif studyday["dayofweek"] == 5:
          studyday["dayofweek"] = 1
        elif studyday["dayofweek"] == 6:
          studyday["dayofweek"] = 2
        elif studyday["dayofweek"] == 7:
          studyday["dayofweek"] = 3
      #third study day or beyond
      if studyday["laststudied"] == "weeklystudy":
        studyday["dayofweek"] = studyday["dayofweek"]
    return newstudydays

  #calgulate what the current day of the week(Sunday,Monday,Tuesday...)
  def currentweekday(self):
    currentweekday = datetime.date.isoweekday((datetime.datetime.utcnow()))
    return currentweekday

  #calculate the sets that should be studied based on the current day of the week
  def todaystudysets(self,newstudydays,currentweekday):
    for item in newstudydays:
      if item["dayofweek"] == currentweekday:
        todaystudysets = [{'title':request["title"],'url':request["url"],'datecreated':time.strftime('%Y-%m-%d',time.localtime(request["created_date"]))} for request in self.setsrequestjson if request["id"] == item["id"]]
    return todaystudysets


  #update histore store for next lookup on sets that are currently being studied
  def updatehistory(self,historystorage,currentweekday):
    for item in historystorage:
       if item["dayofweek"] == currentweekday:
           if item["laststudied"] == "firststudy":
               item["laststudied"] = "secondstudy"
           elif item["laststudied"] == "secondstudy":
               item["laststudied"] = "weeklystudy"
    with open('testdata.json', "w") as f:
      json.dump(historystorage,f)

  def getcurrentsets(self):
    self.ishistoryempty(self.listofids(),self.epochtodate())
    self.addnewsets(self.gethistory())
    todaysets = self.todaystudysets(self.nextstudydays(self.gethistory()),self.currentweekday())
    self.updatehistory(self.gethistory(),self.currentweekday())
    return todaysets
