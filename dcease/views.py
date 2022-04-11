from django.shortcuts import render
from django.http import HttpResponse
from httpx import request
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import numpy as np
import itertools
import re
import speech_recognition as sr
from googletrans import Translator
from translate import Translator
from owlready2 import *

# https://www.google.com/search?q=how+do+you+run+a+python+script+in+django&oq=how+do+you+run+a+python+script+in+django&aqs=chrome..69i57j0i22i30l4j0i390l2.19035j0j7&sourceid=chrome&ie=UTF-8
# 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

# explicit function to take input commands and recognize them
def takeCommandMarathi():

	r = sr.Recognizer()
	with sr.Microphone() as source:
		
		# seconds of non-speaking audio before
		# a phrase is considered complete
		print('Listening')
		r.pause_threshold = 0.7
		audio = r.listen(source)
		try:
			#print("Recognizing")
			Query = r.recognize_google(audio, language='mr-In')
			
			# for listening the command in indian english
			print("the query is printed='", Query, "'")
		
		# handling the exception, so that assistant can
		# ask for telling again the command
		except Exception as e:
			print(e)
			print("Say that again sir")
			return "None"
		return Query

def index(request):
    return render(request, 'index.html', {})

# def speechrecog(request):
#     a=takeCommandMarathi()
#     print(a)
#     return render(request,'page1.html')

# def translate(request):
#     # translate
#     translator = Translator()
#     results = translator.translate(takeCommandMarathi())
#     print(results.text)
#     return HttpResponse(results.text)

def submit(request):
    input = request.GET['transcript']
    translator = Translator(from_lang="Hindi" ,to_lang="English")
    results = translator.translate(input)
    

    # tokenization
    tokens = nltk.word_tokenize(results) 

    # stop word removal   
    stop_words = stopwords.words('english')
    stop_words.append('.') 
    stop_words.append(',') 
    filtered_sentence = []
    for w in tokens:
        if w.lower() not in stop_words:
            filtered_sentence.append(w)

    # pos tagging
    tagged = nltk.pos_tag(filtered_sentence)

    # noun parsing
    new=[]
    for i in tagged:
        if i[1].startswith("NN") or i[1].startswith("RB") or i[1].startswith("JJ") or i[1].startswith("VBG"):
            temp = i[0]
            new.append(temp)

    # lemmatization
    lemmatizer = WordNetLemmatizer()    
    stemmed=[]    
    for w in new:
        stemmed.append(lemmatizer.lemmatize(w))    

    
    # symptom corpus
    # df = pd.read_excel (r'C:\Users\shruti\Downloads\majorproject-master\majorproject-master\Dataset (3).xlsx')
    df = pd.read_excel (r'D:\Sem 7\project\be-project\Dataset (3).xlsx')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.rename(columns = {'snow white hair in patches':'Symptoms'}, inplace = True)
    symptoms = df.values.tolist()
    finalsymp=[]
    symptomsnew =  list(itertools.chain(*symptoms))
    symptomsnew = map(str, symptomsnew) 
    for i in symptomsnew:
        finalsymp.append(str.lower(i))

    output=[]
    for i in stemmed:
        r = re.compile(r'.*('+i+').*')
        for j in finalsymp:
            match = r.search(j)
            if(match is not None and match.group() not in output):
                length = len(match.group().split())
                if(length<=2):
                    output.append(match.group())
                    # output.append(',')
      
    return render(request, 'reconfirm.html', {'stemmed': stemmed,'output': output,'length': len(output)})
    # return HttpResponse(output)

def confirmsymptom(request):
    confirmedsymptoms = request.POST.getlist('symptom1[]')
    
    # convert camel case
    d=[]
    for s in confirmedsymptoms:
        s1 = ''
        s1 += s[0].lower()
        for i in range(1, len(s)):
            if (s[i] == ' '):
                s1 += s[i + 1].upper()
                i += 1
            elif(s[i - 1] != ' '):
                s1 += s[i].lower()
        d.append(s1)

    # load ontology
    # onto_path.append("C:/Users/shruti/Downloads/majorproject-master/majorproject-master")
    # onto=get_ontology("C:/Users/shruti/Downloads/majorproject-master/majorproject-master/latestlatestlatest.owl")
    onto_path.append("D:/Sem 7/project/be-project")
    onto=get_ontology("D:/Sem 7/project/be-project/latestlatestlatest.owl")
    onto.load()

    # inputsymp=list(map(str, input("User symptoms: ").split()))
    n=len(d)
    st='select * where {<http://purl.obolibrary.org/obo/http://www.semanticweb.org/shruti/ontologies/2021/9/untitled-ontology-19#ABCDSyndrome>rdfs:subClassOf?Disease}'
    sym=[]
    for i in d:
        st=st.replace('ABCDSyndrome',i)
        l=list(default_world.sparql(st))
        print(l)
        st=st.replace(i,'ABCDSyndrome')
        for z in range(0,len(l)):
            l1=l[z]
            s=str(l1[0])
            if z==0:
                s=s.replace('untitled-ontology-19.','')
            else:
                s=s.replace('untitled-ontology-19.belongsToDisease.some(untitled-ontology-19.','')
                s=s.replace('untitled-ontology-19.belongsToDisease.some(latestlatestlatest.','')
                s=s.replace(')','')
                sym.append(s)
    return render(request, 'page1.html', {'output': confirmedsymptoms,'ans': sym})
    
def send_disease(request):
    return render(request,'page3.html',context={'text': "Hellow"})