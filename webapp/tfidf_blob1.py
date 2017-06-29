import sys
import math
from textblob import TextBlob as tb
import os
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize

typ=sys.argv[2]
dirc=sys.argv[1]
directory=dirc.replace("\\","\\\\")
##typ='0'
#directory="C:\\InputFiles\\Input6\\"
os.chdir(directory)
c=""
for path,subdirs,files in os.walk(directory):
        #print files
        for filename in files:
            if filename.endswith('.txt'):
                #x=2
                #print filename
                f=open(filename,"r")
                b=f.read().decode('latin-1')
                c=c+b
                f.close()
                #a.write(filename+"\n")
stop_words=set(stopwords.words("english"))
words=word_tokenize(c)
import string
filtered_sent=[]
for w in words:
    if w.lower() not in stop_words:
        filtered_sent.append(w)
d=" ".join(filtered_sent).lower()
import re
d = re.sub(r'[^\w\s]','',d)
list1=d.split()
#print d
from collections import Counter
import operator

counts = Counter(list1)
A=counts
newA = dict(sorted(A.iteritems(), key=operator.itemgetter(1), reverse=True)[:80])
#print newA
if typ=='0':
    from sklearn.cluster import KMeans
    from sklearn.feature_extraction.text import TfidfVectorizer
    t=' '.join(newA.keys())    

    dire="C:\\InputFiles\\corpus\\"
    os.chdir(dire)
    c=""
    maxs=0
    maxn=''
    vectorizer = TfidfVectorizer(min_df=1,lowercase=True)
    for path,subdirs,files in os.walk(dire):
        for filename in files:
            if filename.endswith('.txt'):
                f=open(filename,'r')
                b=f.read().decode('latin-1')
                f.close()
                b.replace('\n',' ')
                texts=[t,b]
                tfidf = vectorizer.fit_transform(texts)
                score=(tfidf*tfidf.T).A[0,1]
                #print filename,(tfidf*tfidf.T).A[0,1]
                if score>maxs:
                    maxs=score
                    maxn=filename
    if maxs>0.1:
        
        print maxn.split("_")[0],maxs
        b=open("C:\\Users\\Administrator\\Desktop\\webapp\\loaded.html","r")
        ft=b.read()
        #print ft
        b.close()
        a=open("C:\\Users\\Administrator\\Desktop\\webapp\\loaded.html","w")
        ind=ft.find('<div class="ntext">')
        a.write(ft[:ind])
        a.write('<div class="ntext">This corpus is about '+maxn.split('_')[0]+'.')
        ind2=ft.find('</div>',ind)
        a.write(ft[ind2:])
        a.close()

    else:
        print maxn.split("_")[0],maxs
        b=open("C:\\Users\\Administrator\\Desktop\\webapp\\loaded.html","r")
        ft=b.read()
        #print ft
        b.close()
        a=open("C:\\Users\\Administrator\\Desktop\\webapp\\loaded.html","w")
        ind=ft.find('<div class="ntext">')
        a.write(ft[:ind])
        a.write('<div class="ntext">We think this corpus is about '+maxn.split('_')[0]+'. But we are not sure.')
        ind2=ft.find('</div>',ind)
        a.write(ft[ind2:])
        a.close()


else:
    fname="C:\\InputFiles\\corpus\\"+typ+"_corpus.txt"
    f=open(fname,"w")
    for k in newA:
        f.write(k+'\n')
    f.close()
  


#####tfidf########
#bloblist = [document1]
#for i, blob in enumerate(bloblist):
#    print("Top words in document {}".format(i + 1))
##print 'i am here',len(blob.words)
##scores = {word: tf(word, blob) for word in blob.words}
##print 'thats done now here'
##sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
##print 'sorted arent i'
##for word, score in sorted_words[:10]:
##    print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
