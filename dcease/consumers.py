from itertools import count
from channels.generic.websocket import WebsocketConsumer
import json
from random import randint
from time import sleep
from .connection import *
from .views import sym,d
from owlready2 import *
from owlready2.sparql.endpoint import *

onto_path.append("D:/Sem 7/project/ontology versions")
onto=get_ontology("D:/Sem 7/project/ontology versions/latestlatestlatest.owl")
# onto_path.append("C:/Users/shruti/Downloads/majorproject-master/majorproject-master")
# onto=get_ontology("C:/Users/shruti/Downloads/majorproject-master/majorproject-master/latestlatestlatest.owl")
onto.load()
# countdic={}
# print(sym)
# for i in sym:
#     if i not in countdic:
#         countdic[i]=1
#     else:
#         countdic[i]=countdic[i]+1
# countdic=(dict(sorted(countdic.items(), key=lambda item: item[1], reverse= 1)))

class WSConsumer(WebsocketConsumer):
    countdic={}
    def connect(self):
        print(sym)
        c={}
        for i in sym:
            if i not in c:
                c[i]=1
            else:
                c[i]=c[i]+1
        WSConsumer.countdic=(dict(sorted(c.items(), key=lambda item: item[1], reverse= 1)))
        for i in WSConsumer.countdic:
            WSConsumer.countdic[i]=int(WSConsumer.countdic[i]/2)
        self.accept()

    def receive(self,text_data):
        text_data=text_data[1:len(text_data)-1]
        print(text_data)
        # if text_data=="ABCDSyndrome":
        #     l=[]
        #     l,p=disease('ABCDSyndrome')
        #     k=list(set(l))
        #     m='untitled-ontology-19.'+p
        #     if m in k:
        #         k.remove(m)
        #     self.send(json.dumps({'message':p,'message1':k}))
        #     sleep(5)
        # elif text_data=="AMEDSyndrome":
        #     l=[]
        #     l,p=disease('AMEDSyndrome')
        #     k=list(set(l))
        #     m='untitled-ontology-19.'+p
        #     if m in k:
        #         k.remove(m)
        #     self.send(json.dumps({'message':p,'message1':k}))
        #     sleep(1)
        if text_data=="yes":
            # self.send(json.dumps({'message':sym,'message1':"ko"}))   
            print(WSConsumer.countdic)
            lst=[]
            n=len(d)
            print(d)
            if n == WSConsumer.countdic[list(WSConsumer.countdic.keys())[0]]:
                lst.append(list(WSConsumer.countdic.keys())[0])
                l,p=disease(lst[-1])
                l.remove('untitled-ontology-19.'+p)
                l=list(set(l))
                self.send(json.dumps({'message':"Disease Name:",'message1':list(WSConsumer.countdic.keys())[0],'message2':p,'message3':l,'message4':"Want to move forward?"}))
                WSConsumer.countdic.pop(list(WSConsumer.countdic.keys())[0])
                # print("Disease Name:",key)
                # print("Do you wish to know if these diseases have any other symptoms??")
                # ans=input("y/n")
                # self.send(json.dumps({'message':p,'message1':l,'message2':"Want to move forward?"})) 
                # print("Symptoms: ",l)
                # print("Want to move forward?")
                # ans=input("y/n?")
            else:
                # self.send(json.dumps({'message':"Symptoms",'message1':l,'message2':"Want to move forward?"})) 
                # print("No diseases found for the exact combination of symptoms entered. Trying to find closest matches.....")
                while(n>2):
                    n=n-1
                    if n == WSConsumer.countdic[list(WSConsumer.countdic.keys())[0]]:
                        lst.append(list(WSConsumer.countdic.keys())[0])
                        l,p=disease(lst[-1])
                        self.send(json.dumps({'message':"Disease Name:",'message1':list(WSConsumer.countdic.keys())[0],'message2':p,'message3':l,'message4':"Want to move forward?"}))
                        sleep(10)
                        # print("Disease Name:",key)
                        # print("Do you wish to know if these diseases have any other symptoms??")
                        # ans=input("y/n")
                        # print("Symptoms: ",l)
                        # # print("Matching symptoms are:",)
                        # print("Want to move forward?")
                        # ans=input("y/n?")
                    # if value == n:
                    #     lst.append(key)
                # break
        # if lst==[]:
        #     self.send(json.dumps({'message':"No match found for the combination of symptoms entered. Kindly reassess your symptoms and try again!"})) 
                    
            # print("No match found for the combination of symptoms entered. Kindly reassess your symptoms and try again!")
        else:
            self.close()