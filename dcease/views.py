from django.shortcuts import render
from django.http import HttpResponse
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import numpy as np
import itertools
import re
import speech_recognition as sr

def index(request):
    return render(request, 'index.html', {})

def submit(request):
    input = request.GET['symptoms']

    # translate

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
    df = pd.read_excel (r'C:\Users\shruti\Downloads\Dataset (3).xlsx')
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