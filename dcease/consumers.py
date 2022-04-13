from channels.generic.websocket import WebsocketConsumer
import json
from random import randint
from time import sleep
from .connection import *
from owlready2 import *
from owlready2.sparql.endpoint import *

onto_path.append("D:/Sem 7/project/ontology versions")
onto=get_ontology("D:/Sem 7/project/ontology versions/latestlatestlatest.owl")
# onto_path.append("C:/Users/shruti/Downloads/majorproject-master/majorproject-master")
# onto=get_ontology("C:/Users/shruti/Downloads/majorproject-master/majorproject-master/latestlatestlatest.owl")
 
onto.load()
class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # if text_data=='TESTEST':
        #     self.send(json.dumps({'message':p}))
        # self.send(json.dumps({'message1':l}))
        # for i in range(1000):
        #     self.send(json.dumps({'message':randint(1,100)}))
        #     sleep(1)

    def receive(self,text_data):
        text_data=text_data[1:len(text_data)-1]
        print(text_data)
        if text_data=="ABCDSyndrome":
            l=[]
            l,p=disease('ABCDSyndrome')
            k=list(set(l))
            m='untitled-ontology-19.'+p
            if m in k:
                k.remove(m)
            self.send(json.dumps({'message':p,'message1':k}))
            sleep(5)
        elif text_data=="AMEDSyndrome":
            l=[]
            l,p=disease('AMEDSyndrome')
            k=list(set(l))
            m='untitled-ontology-19.'+p
            if m in k:
                k.remove(m)
            self.send(json.dumps({'message':p,'message1':k}))
        else:
            self.close()