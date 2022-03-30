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
# https://www.google.com/search?q=how+do+you+run+a+python+script+in+django&oq=how+do+you+run+a+python+script+in+django&aqs=chrome..69i57j0i22i30l4j0i390l2.19035j0j7&sourceid=chrome&ie=UTF-8
# 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

# explicit function to take input commands and recognize them
def takeCommandMarathi():

	r = sr.Recognizer()
	with sr.Microphone() as source:
		
		# seconds of non-speaking audio before
		# a phrase is considered complete
		#print('Listening')
		r.pause_threshold = 0.7
		audio = r.listen(source)
		try:
			#print("Recognizing")
			Query = r.recognize_google(audio, language='mr-In')
			
			# for listening the command in indian english
			#print("the query is printed='", Query, "'")
		
		# handling the exception, so that assistant can
		# ask for telling again the command
		except Exception as e:
			print(e)
			print("Say that again sir")
			return "None"
		return Query

def index(request):
    return render(request, 'index.html', {})

def speechrecog(request):
    a=takeCommandMarathi()
    print(a)
    return render(request,'index.html',{'a':a})

def translate(request):
    # translate
    translator = Translator()
    results = translator.translate(takeCommandMarathi())
    #print(results.text)
    return HttpResponse(results.text)

def submit(request):
    input = request.GET['symptoms']

    # tokenization
    tokens = nltk.word_tokenize(input) 

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
            if(match is not None):
                length = len(match.group().split())
                if(length<=3):
                    output.append(match.group())
                    output.append(',')

    # for k in output:
    #     print(k,end="")
    # return render(request, 'page1.html', {'output': stemmed})
    return HttpResponse(output)