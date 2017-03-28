import requests,pprint,datetime,time,json,os,itertools
from studysets import StudySets

setsrequest = requests.get('https://api.quizlet.com/2.0/users/wuzza_face/sets/?client_id=pyjFb2bnBN')
setsrequestjson = setsrequest.json()

new = StudySets(setsrequestjson)

'''
print(new.epochtodate())
print(new.listofids())
print(new.ishistoryempty(new.listofids(),new.epochtodate()))
print(new.gethistory())
print(new.addnewsets(new.gethistory()))
print(new.nextstudydays(new.gethistory()))
print(new.currentweekday())
print(new.todaystudysets(new.nextstudydays(new.gethistory()),new.currentweekday()))
print(new.updatehistory(new.gethistory(),new.currentweekday()))
'''

print(new.getcurrentsets())
