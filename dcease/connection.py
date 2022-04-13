from os import lstat
from pickle import TRUE
from owlready2 import *
from owlready2.sparql.endpoint import *

onto_path.append("D:/Sem 7/project/ontology versions")
onto=get_ontology("D:/Sem 7/project/ontology versions/latestlatestlatest.owl")
# onto_path.append("C:/Users/shruti/Downloads/majorproject-master/majorproject-master")
# onto=get_ontology("C:/Users/shruti/Downloads/majorproject-master/majorproject-master/latestlatestlatest.owl")
 
onto.load()

#Function for finding symptoms based on diseases
def disease(name):

    st='select * where {<http://purl.obolibrary.org/obo/http://www.semanticweb.org/shruti/ontologies/2021/9/untitled-ontology-19#ABCDSyndrome>rdfs:subClassOf?Symptom}'
    st=st.replace('ABCDSyndrome',name)
    l=list(default_world.sparql(st))
    # for i in l:
    #     print(i)
    #print(l)
    st=st.replace(name,'ABCDSyndrome')
    sym=[]
    parent=''
    for z in range(0,len(l)):
        l1=l[z]
        s=str(l1[0])
        if z==0:
            s=s.replace('untitled-ontology-19.','')
            parent=s
        else:
            s=s.replace('untitled-ontology-19.hasSymptom.some(untitled-ontology-19.','')
            s=s.replace(')','')
            sym.append(s)
    return sym,parent
    # print(sym)
    # print(parent)
# disease(input("Name of Disease:"))


# Function for finding disease based on symptoms-> input symptoms in list of strings format
def symptoms(inputsymp):
    # inputsymp=list(map(str, input("User symptoms: ").split()))
    # n=len(inputsymp)
    st='select * where {<http://purl.obolibrary.org/obo/http://www.semanticweb.org/shruti/ontologies/2021/9/untitled-ontology-19#ABCDSyndrome>rdfs:subClassOf?Disease}'
    sym=[]
    for i in inputsymp:
        st=st.replace('ABCDSyndrome',i)
        l=list(default_world.sparql(st))
        # print(l)
        st=st.replace(i,'ABCDSyndrome')
        for z in range(0,len(l)):
            l1=l[z]
            s=str(l1[0])
            if z==0:
                s=s.replace('untitled-ontology-19.','')
                parent=s
            else:
                s=s.replace('untitled-ontology-19.belongsToDisease.some(untitled-ontology-19.','')
                s=s.replace('untitled-ontology-19.belongsToDisease.some(latestlatestlatest.','')
                s=s.replace(')','')
                sym.append(s)
    return sym

#Making countdic of disease-noof symptoms(noof=number of)-> input symptoms in list of strings format
def dictionary(inputsymp):
    sym=symptoms(inputsymp)   
    countdic={}
    for i in sym:
        if i not in countdic:
            countdic[i]=1
        else:
            countdic[i]=countdic[i]+1
    countdic=(dict(sorted(countdic.items(), key=lambda item: item[1], reverse= 1)))
    return countdic

#Interaction with the user to narrow down on the disease-> input symptoms in list of strings format
def interaction(inputsymp):
    lst=[]
    ct=0
    n=len(inputsymp)
    countdic=dictionary(inputsymp)
    for key, value in countdic.items():
        if n == value:
            print("Disease Name:",key)
            lst.append(key)
            print("Do you wish to know if these diseases have any other symptoms??")
            ans=input("y/n")
            if ans=='n':
                break
            else:
                for i in range (ct,len(lst)):
                    flag=0
                    l,p=disease(lst[i])
                    print("Symptoms: ",l)
                    print("Want to move forward?")
                    ans=input("y/n?")
                    if ans=='n':
                        flag=1
                        break
            ct=ct+1
            if(flag==1):
                break
        else:
            print("No diseases found for the exact combination of symptoms entered. Trying to find closest matches.....")
            while(n>2):
                n=n-1
                for key, value in countdic.items():
                    if n == value:
                        print("Disease Name:",key)
                        lst.append(key)
                        print("Do you wish to know if these diseases have any other symptoms??")
                        ans=input("y/n")
                        if ans=='n':
                            break
                        else:
                            for i in range (ct,len(lst)):
                                flag=0
                                l,p=disease(lst[i])
                                print("Symptoms: ",l)
                                # print("Matching symptoms are:",)
                                print("Want to move forward?")
                                ans=input("y/n?")
                                if ans=='n':
                                    flag=1
                                    break
                        ct=ct+1
                        print(ct)
                        if(flag==1):
                            break
                # if value == n:
                #     lst.append(key)
                if lst!=[]:
                    break
            break
    if lst==[]:
        print("No match found for the combination of symptoms entered. Kindly reassess your symptoms and try again!")

q=['cough','fever']
print(disease('AMEDSyndrome'))
print('-------------------------------------')
print(set(symptoms(q)))
print('-------------------------------------')
print(dictionary(q))
print('-------------------------------------')
interaction(q)

# if lst !=[]:
#     print(lst)
#     flag=0
#     for i in lst:
#         print("Do you have the following symptoms: ")
#         disease(i)
#         ans=input("y/n?")
#         if ans=='y':
#             flag=1
#             break
#     if flag==0:
#         print("Kindly reassess your symptoms and try again!")
# print(countdic)

# NONFUNCTIONAL OR PREVIOUSLY IMPLEMENTED PART BELOW.

# # #code to convert to camel case
# # def camelCase(s):
# #     if(len(s) == 0):
# #         return
# #     s1 = ''
# #     s1 += s[0].lower()
# #     for i in range(1, len(s)):
# #         if (s[i] == ' '):
# #             s1 += s[i + 1].upper()
# #             i += 1
# #         elif(s[i - 1] != ' '):
# #             s1 += s[i].lower()
# #     return s1

# # print(camelCase('MILD fEVER'))

# import speech_recognition as sr
# # explicit function to take input commands
# # and recognize them
# def takeCommandMarathi():

# 	r = sr.Recognizer()
# 	with sr.Microphone() as source:
		
# 		# seconds of non-speaking audio before
# 		# a phrase is considered complete
# 		print('Listening')
# 		r.pause_threshold = 0.7
# 		audio = r.listen(source)
# 		try:
# 			print("Recognizing")
# 			Query = r.recognize_google(audio, language='mr-In')
			
# 			# for listening the command in indian english
# 			print("the query is printed='", Query, "'")
		
# 		# handling the exception, so that assistant can
# 		# ask for telling again the command
# 		except Exception as e:
# 			print(e)
# 			print("Say that again sir")
# 			return "None"
# 		return Query

# from googletrans import Translator
# translator = Translator()
# results = translator.translate(takeCommandMarathi())
# print(results.text)

# newq='select * where {<http://purl.obolibrary.org/obo/http://www.semanticweb.org/shruti/ontologies/2021/9/untitled-ontology-19#ABCDSyndrome>rdfs:subClassOf?Disease}'
# k=default_world.sparql(newq)
# print(type(k))
# print(k)

# graph = default_world.as_rdflib_graph()
# r = (graph.query("""SELECT * WHERE {
#   <http://purl.obolibrary.org/obo/http://www.semanticweb.org/shruti/ontologies/2021/9/untitled-ontology-19#ABCDSyndrome> rdfs:subClassOf ?Disease}"""))
# print(r)
# print(type(r))
# G= rdflib_to_networkx_multidigraph(r)
# nx.draw(G)
# plt.show()
# # print(graph)


# st='select * where {<http://purl.obolibrary.org/obo/http://www.semanticweb.org/shruti/ontologies/2021/9/untitled-ontology-19#ABCDSyndrome>rdfs:subClassOf?Disease}'
#select ?Symtom where {<http://purl.obolibrary.org/obo/http://www.semanticweb.org/shruti/ontologies/2021/9/untitled-ontology-19#fever> rdfs:subClassOf  ?Symtom}
# print(onto.individuals)
# print(list(onto.classes()))