import sys
#y=sys.argv[1]

import os
import re
from textblob import TextBlob
import json
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
import operator

food=['food','eat','meal','meals','eating','drink','drinks','beer','juice']
staff=['staff','waiter','waiters','worker','workers']
service=['serve','service','serving']
ambience=['ambience','atmosphere','luxury','music','lighting','place','view','pool','events']
    
table={}
tab={}
resnames=[]
def category(sentence):
    
    stop_words=set(stopwords.words("english"))
    words=word_tokenize(sentence)
    filtered_sent=[]
    for w in words:
        if w not in stop_words:
            filtered_sent.append(w)
    b=filtered_sent
    #print b
    cat=[]
    #b=sentence.lower().split()
    if (set(food)&set(b)):
        cat.append('Food')
    if (set(staff)&set(b)):
        cat.append('Staff')
    if (set(service)&set(b)):
        cat.append('Service')
    if (set(ambience)&set(b)):
        cat.append('Ambience')
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
    global resnames
    if res not in resnames:
        resnames.append(res)
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

    global tab
    if date in tab:
        if res not in tab[date]:
            tab[date][res]=[]
    else:
        tab[date]={}
        tab[date][res]=[]
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
        tab[date][res].append(t.sentiment.polarity)
        #print(t.sentiment)
        sentences.append('{"Sentence":'+'"'+s+'", '+'"Sentiment polarity":'+x+'}')
        sents.append('Sentence : '+'"'+s+'"'+', Sentiment Polarity : '+x)
        htmls.append("<tr><td>"+res+"</td><td>"+date+"</td><td>"+str(i)+"</td><td>"+s+"</td><td>"+categ+"</td><td>"+x+"</td></tr>")
    result='{"Result": ['+','.join(sentences)+'] }'
    #print result
    jo=json.loads(result)
    a=open("C:\\Users\\Abha Saxena\\Desktop\\webapp\\w1.json","w")
    a.write(result)
    a.close()
    b=open("C:\\Users\\Abha Saxena\\Desktop\\webapp\\index.html","r")
    ft=b.read()
    #print ft
    b.close()
    a=open("C:\\Users\\Abha Saxena\\Desktop\\webapp\\index.html","w")
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
    #dirc = sys.argv[1]
    dirc = "C:\\Python27\\xyz"
    #os.chdir(dir)
    directory=dirc.replace("\\","\\\\")
    #print directory
    #a=open("w1.txt","w")
    b=open("C:\\Users\\Abha Saxena\\Desktop\\webapp\\index.html","r")
    ft=b.read()
    #print ft
    b.close()
    a=open("C:\\Users\\Abha Saxena\\Desktop\\webapp\\index.html","w")
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
    data="function drawBasic() {\n"
    global table
    print table
    i=1
    for k1 in table:
        for k2 in table[k1]:
            for k3 in table[k1][k2]:
                z=sum(table[k1][k2][k3])/float(len(table[k1][k2][k3]))
                print k1,k2,k3,z
                table[k1][k2][k3]=z
    #a.close()
        x=["['Category','Sentiment Score',]"]
        xx={}
    #print table
    
        for k2 in table[k1]:
            xx[k2]=datetime.strptime(k2, '%d-%m-%y')
        print xx
        m= max(xx.iteritems(), key=operator.itemgetter(1))[0]
        
        for k in table[k1][m]:
            print k,table[k1][m][k]
            x.append("['"+k+"',"+("%.2f"%table[k1][m][k])+"]")
        y="var data"+str(i)+"=google.visualization.arrayToDataTable([\n"+",".join(x)+"\n]);\n"
        data=data+y
        i=i+1
    data=data+"var chart = new google.visualization.BarChart(document.getElementById('chart_div1'));\n"
    for j in range(1,i):
        data=data+"\nif(flag=="+str(j)+") chart.draw(data"+str(j)+", options);"
    data=data+"\n}\n"
    print data
    
    #print ft
    b=open("C:\\Users\\Abha Saxena\\Desktop\\webapp\\index.html","r")
    ft=b.read()
    b.close()
    a=open("C:\\Users\\Abha Saxena\\Desktop\\webapp\\index.html","w")
    ind=ft.find("function drawBasic() {")
    a.write(ft[:ind])
    a.write(data)
    ind3=ft.find("</script>",ind)
    a.write(ft[ind3:])
    a.close()

    b=open("C:\\Users\\Abha Saxena\\Desktop\\webapp\\index.html","r")
    ft=b.read()
    b.close()
    a=open("C:\\Users\\Abha Saxena\\Desktop\\webapp\\index.html","w")
    ind=ft.find('<select id="Ultra"')
    a.write(ft[:ind])
    a.write('<select id="Ultra" onchange="run()">\n<option value="0">Select Restaurant</option>\n')
    i=1
    for k in table:
        a.write('<option value="'+str(i)+'">'+k+'</option>\n')
        i=i+1
    ind3=ft.find("</select>",ind)
    a.write(ft[ind3:])
    a.close()
    global tab
    print tab
    for k1 in tab:
        for k2 in tab[k1]:
            tab[k1][k2]=sum(tab[k1][k2])/float(len(tab[k1][k2]))
    print tab
    x1=[]
    for k1 in tab:
        d=datetime.strptime(k1, '%d-%m-%y')
        print "year:{0:%Y}, month:{0:%m}, day:{0:%d}".format(d)
        d1="new Date({0:%Y},{0:%m},{0:%d})".format(d)
        
        for r in resnames:
            d1=d1+","+"%.2f"%tab[k1][r]
        x1.append("["+d1+"]")
    y1="data.addRows(["+",".join(x1)+"]);"
    print y1
    b=open("C:\\Users\\Abha Saxena\\Desktop\\webapp\\index.html","r")
    ft=b.read()
    b.close()
    a=open("C:\\Users\\Abha Saxena\\Desktop\\webapp\\index.html","w")
    ind=ft.find('function drawLineStyles()')
    a.write(ft[:ind])
    a.write("function drawLineStyles() {\nvar data = new google.visualization.DataTable();\ndata.addColumn('date', 'Date');\n")
    for r in resnames:
        a.write("data.addColumn('number','"+r+"');\n")
    a.write(y1+"\n")
    ind3=ft.find("var chart1",ind)
    a.write(ft[ind3:])
    a.close()
