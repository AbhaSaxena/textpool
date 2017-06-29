import sys
#y=sys.argv[1]

import os
import re
from textblob import TextBlob
import json
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
import operator
import string
import collections
from nltk.stem import PorterStemmer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from datetime import datetime
##food=['food','eat','meal','meals','eating','drink','drinks','beer','juice']
##staff=['staff','waiter','waiters','worker','workers']
##service=['serve','service','serving']
##ambience=['ambience','atmosphere','luxury','music','lighting','place','view','pool','events']

table={}

def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation """
    #text = text.translate(None,string.punctuation)
    tokens = word_tokenize(text)
 
    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]
 
    return tokens
 
 
def sim(texts):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 min_df=1,
                                 lowercase=True)
 
    tfidf = vectorizer.fit_transform(texts)
    return (tfidf*tfidf.T).A[0,1]
    

def category(s):
    fd=open("C://Python27//restaurant//food.txt")
    #global food
    food=fd.read().decode('latin-1')
    #ambience=newcorpus.open("ambience.txt").read().encode('utf-8')
    am=open("C://Python27//restaurant//ambience.txt")
    #global ambience
    ambience=am.read().decode('latin-1')
    sr=open("C://Python27//restaurant//service.txt")
    #global ambience
    service=sr.read().decode('latin-1')
    fd.close()
    am.close()
    sr.close()
    cat=[]
    texts=[s,food]
    texts2=[s,ambience]
    texts3=[s,service]
    if(sim(texts)!=0):
        cat.append('food')
    if(sim(texts2)!=0):
        cat.append('ambience')
    if(sim(texts3)!=0):
        cat.append('service')
    
    return cat 

def fun(dirctry,fname):
    os.chdir(dirctry)
    f = open(fname,'r')
    p=f.read()
    #print "****",p
    q = p.replace("\n"," ")
    #print "----",q
    regexMatch = re.findall('[^.!?)]+[.!?)]+',q)
    #print "####",regexMatch
    f.close()
    name_date=fname.split("_")
    res=name_date[0]
    
    
    d=name_date[1].replace(".txt","")
    date='-'.join(a+b for a,b in zip(d[::2], d[1::2]))
    sentences=[]
    sents=[]
    htmls=[]

    global table
    if res in table:
        table[res][date]={}
    else:
        table[res]={}
        table[res][date]={}
    
    i=0
    for s in regexMatch:
        #print "$$$$",s
        i=i+1
        #print(s)
        t=TextBlob(s)
        ca=category(s)
        categ=", ".join(ca)
        for c in ca:
            if c in table[res][date]:
                table[res][date][c].append(t.sentiment.polarity)
            else:
               table[res][date][c]=[]
               table[res][date][c].append(t.sentiment.polarity)
        x="%.2f" % t.sentiment.polarity
        #print(t.sentiment)
        sentences.append('{"Sentence":'+'"'+s+'", '+'"Sentiment polarity":'+x+'}')
        sents.append('Sentence : '+'"'+s+'"'+', Sentiment Polarity : '+x)
        htmls.append("<tr><td>"+res+"</td><td>"+date+"</td><td>"+str(i)+"</td><td>"+s+"</td><td>"+categ+"</td><td>"+x+"</td></tr>")
    result='{"Result": ['+','.join(sentences)+'] }'
    #print result
    jo=json.loads(result)
    a=open("C:\\Users\\Administrator\\Desktop\\webapp\\w1.json","w")
    a.write(result)
    a.close()
    b=open("C:\\Users\\Administrator\\Desktop\\webapp\\index.html","r")
    ft=b.read()
    #print ft
    b.close()
    a=open("C:\\Users\\Administrator\\Desktop\\webapp\\index.html","w")
    ind=ft.find("<tbody>")+8
    ind2=ft.find("</tbody>")
    a.write(ft[:ind2])
    for h in htmls:
        a.write(h+"\n")
    #ind3=ft.find("</tbody>")
    a.write(ft[ind2:])
    a.close()

    return

if __name__=="__main__":
    #fun("C:\Python27",sys.argv[1])
    #dirc = raw_input("Enter the directory where the files are stored in: ")
    dirc = "C:\\Python27\\xyz"
    #os.chdir(dir)
##    fd=open("C://Python27//restaurant//food.txt")
##    #global food
##    
##    food=fd.read().decode('latin-1')
##    #ambience=newcorpus.open("ambience.txt").read().encode('utf-8')
##    am=open("C://Python27//restaurant//ambience.txt")
##    #global ambience
##    ambience=am.read().decode('latin-1')
    directory=dirc.replace("\\","\\\\")
    #print directory
    #a=open("w1.txt","w")
    b=open("C:\\Users\\Administrator\\Desktop\\webapp\\index.html","r")
    ft=b.read()
    #print ft
    b.close()
    a=open("C:\\Users\\Administrator\\Desktop\\webapp\\index.html","w")
    ind=ft.find("<tbody>")+8
    a.write(ft[:ind])
    ind3=ft.find("</tbody>")
    a.write(ft[ind3:])
    a.close()
    for path,subdirs,files in os.walk(directory):
        #print files
        for filename in files:
            if filename.endswith('.txt'):
                #x=2
                #print filename
                fun(directory,filename)
                #a.write(filename+"\n")
    global table
    print table
    for k1 in table:
        for k2 in table[k1]:
            for k3 in table[k1][k2]:
                z=sum(table[k1][k2][k3])/float(len(table[k1][k2][k3]))
                print k1,k2,k3,z
                table[k1][k2][k3]=z
    #a.close()
        x={}            
    #print table
    
        for k2 in table[k1]:
            x[k2]=datetime.strptime(k2, '%d-%m-%y')
        print x
        m= max(x.iteritems(), key=operator.itemgetter(1))[0]
        for k in table[k1][m]:
            print k,table[k1][m][k]
