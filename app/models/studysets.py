import requests,pprint,datetime,time,json,os,itertools

class StudySets:

  def __init__(self,setsrequestjson):
    self.setsrequestjson = setsrequestjson  #current information for the public decks of the user from quizlet's api

  #a list of days that the decks were created
  #the day of the week is represented as a numerical value (1-7:Mon-Sun)
  def epochtodate(self):
    days = ([datetime.date.isoweekday(datetime.date.fromtimestamp(item["created_date"])) for item in self.setsrequestjson])
    return days

  #a list of id's for all of the decks that were imported
  def listofids(self):
    ids = ([item["id"]for item in self.setsrequestjson])	
    return ids

  #if the history storage is empty, store the needed data from setsrequestjson
  #needed data includes the id number, day of the week the deck was created, and an initial last studied value of "first study"
  def ishistoryempty(self,ids,days):
    if os.stat("testdata.json").st_size == 0:
      initialhistorydata = [{'id': idnum, 'laststudied': freq, 'dayofweek': day} for idnum, freq, day in zip(ids,itertools.repeat('firststudy'),days)]
      with open('testdata.json', 'w') as f:
        json.dump(initialhistorydata,f)

  #retrieve the currently stored set data from history storage
  def gethistory(self):
    with open('testdata.json', "r") as f:
      historystorage = json.load(f)
    return historystorage

  #check if any new sets have been added since the last update to history storage. Add any new sets to the history storage with a last studied value of "first study"
  def addnewsets(self,historystorage):
    historyids = ([item["id"]for item in historystorage])	
    for set in self.setsrequestjson:
      if set["id"] not in historyids:
        historystorage.append({'id': set["id"],'laststudied': 'firststudy','dayofweek': datetime.date.isoweekday(datetime.date.fromtimestamp(set["created_date"]))}) 

  def incrementstudyday(value, i):
    return (value - 1) % 7 + 1

  #determine the week day that each deck should study based on the history storage
  #counting from the week day that the deck was created, firststudy advances by 1 day, secondstudy by 3, and weeklystudy is the same day of the week as the initial deck creation.
  def nextstudydays(self,historystorage):
    daystoprogress = {"firststudy" : 1,
                      "secondstudy" : 3}
    newstudydays = historystorage
    daystoprogress = 0
    for studyday in newstudydays:
      studyday["dayofweek"] = incrementstudyday(studyday["dayofweek"], daystoprogress.get(studyday["laststudied"], 0))
    return newstudydays

  #calculates current day of the week and returns a corresponding numeric value
  def currentweekday(self):
    currentweekday = datetime.date.isoweekday((datetime.datetime.utcnow()))
    return currentweekday

  #calculates the sets that should be studied today based on the current day of the week
  def todaystudysets(self,newstudydays,currentweekday):
    for item in newstudydays:
      if item["dayofweek"] == currentweekday:
        todaystudysets = [{'title':request["title"],'url':request["url"],'datecreated':time.strftime('%Y-%m-%d',time.localtime(request["created_date"]))} for request in self.setsrequestjson if request["id"] == item["id"]]
    return todaystudysets


  #updates the history storage so that the last studied value is accurately reflected
  def updatehistory(self,historystorage,currentweekday):
    for item in historystorage:
       if item["dayofweek"] == currentweekday:
           if item["laststudied"] == "firststudy":
               item["laststudied"] = "secondstudy"
           elif item["laststudied"] == "secondstudy":
               item["laststudied"] = "weeklystudy"
    with open('testdata.json', "w") as f:
      json.dump(historystorage,f)

  #returns the sets that need to be studied today as a list of dictionaries that include a title, url, and date of creation
  def getcurrentsets(self):
    self.ishistoryempty(self.listofids(),self.epochtodate())
    self.addnewsets(self.gethistory())
    todaysets = self.todaystudysets(self.nextstudydays(self.gethistory()),self.currentweekday())
    self.updatehistory(self.gethistory(),self.currentweekday())
    return todaysets
