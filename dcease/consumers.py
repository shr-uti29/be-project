from channels.generic.websocket import WebsocketConsumer
import json
from random import randint
from time import sleep
# from .connection import *
from owlready2 import *
from owlready2.sparql.endpoint import *

onto_path.append("D:/Sem 7/project/ontology versions")
onto=get_ontology("D:/Sem 7/project/ontology versions/latestlatestlatest.owl")
onto.load()

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # l,p=disease('AMEDSyndrome')
        # print(l)
        # for i in range(0,len(l)):
        #     s=l[i]
        #     self.send(json.dumps({'message':s}))
        # self.send(json.dumps({'message1':p}))
        for i in range(1000):
            self.send(json.dumps({'message':randint(1,100)}))
            sleep(1)