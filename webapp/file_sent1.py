import sys
#y=sys.argv[1]

import os
import re
from textblob import TextBlob
import json
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


food=['food','eat','meal','meals','eating','drink','drinks','beer','juice']
staff=['staff','waiter','waiters','worker','workers']
service=['serve','service','serving']
ambience=['ambience','atmosphere','luxury','music','lighting','place','view','pool','events']
vect= TfidfVectorizer(min_df=1)

def category(sentence):
    
    stop_words=set(stopwords.words("english"))
    words=word_tokenize(sentence.lower())
    filtered_sent=[]
    for w in words:
        if w not in stop_words:
            filtered_sent.append(w)
    b=" ".join(filtered_sent)
    #print b
    cat=[]
    for s in food:
        pair=[b,s]
        tfidf=vect.fit_transform(pair)
        if (tfidf*tfidf.T).A[0,1]>=0.3:
            cat.append('food')
            food.append(b)
            break
    for s in staff:
        pair=[b,s]
        tfidf=vect.fit_transform(pair)
        if (tfidf*tfidf.T).A[0,1]>=0.3:
            cat.append('staff')
            staff.append(b)
            break
    for s in service:
        pair=[b,s]
        tfidf=vect.fit_transform(pair)
        if (tfidf*tfidf.T).A[0,1]>=0.3:
            cat.append('service')
            service.append(b)
            break
    for s in ambience:
        pair=[b,s]
        tfidf=vect.fit_transform(pair)
        if (tfidf*tfidf.T).A[0,1]>=0.3:
            cat.append('ambience')
            ambience.append(b)
            break
    
    #b=sentence.lower().split()
##    if (set(food)&set(b)):
##        cat.append('Food')
##    if (set(staff)&set(b)):
##        cat.append('Staff')
##    if (set(service)&set(b)):
##        cat.append('Service')
##    if (set(ambience)&set(b)):
##        cat.append('Ambience')
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
    i=0
    for s in regexMatch:
        #print "$$$$",s
        i=i+1
        #print(s)
        t=TextBlob(s)
        categ=", ".join(category(s))
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
    dirc = sys.argv[1]
    #os.chdir(dir)
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
    #a.close()
