from textblob.classifiers import NaiveBayesClassifier as NBC
from textblob import TextBlob

#f=open("w2.txt","a")

##a=open("restaurant//food.txt","r")
##b=a.read()
##a.close()
##c=b.split("\n")
##d=[]
##for s in c:
##    d.append(s+"$$$food")
##res='\n'.join(d)
###print res
##f.write('\n')
##f.write(res)

##a=open("restaurant//ambience.txt","r")
##b=a.read()
##a.close()
##c=b.split("\n")
##d=[]
##for s in c:
##    d.append(s+"$$$ambience")
##res='\n'.join(d)
###print res
##f.write('\n')
##f.write(res)
##
##a=open("restaurant//service.txt","r")
##b=a.read()
##a.close()
##c=b.split("\n")
##d=[]
##for s in c:
##    d.append(s+"$$$service")
##res='\n'.join(d)
###print res
##f.write('\n')
##f.write(res)
##f.close()

f=open("w2.txt","r")
p=f.read().decode('latin-1')
sentences=p.split('\n')
#print sentences
training_corpus=[]
for s in sentences:
    t=s.split('$$$')
    #print t
    if len(t)==2:
        training_corpus.append(tuple(t))
#print training_corpus
model = NBC(training_corpus) 
print(model.classify("the service is very quick and they treated us with courtesy."))
f.close()
