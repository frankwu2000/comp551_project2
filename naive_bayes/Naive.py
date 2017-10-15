import csv
import sys
import re
import itertools

reload(sys)
sys.setdefaultencoding('utf8')
sys.maxunicode
prase_data=[]
class_probability=[]
Dicts=[]

occur_plus_vocabulary=[]
#f=open('myfile.txt','w')
i=0
myre = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')


def paraseData_ngram(n,Dicts,occur_plus_vocabulary):
    occur=[]
    vocabulary=0
    for x in range(0,5):
        Dicts+=[{}]
    with open('train_set_x.csv','rb') as trainx, open('train_set_y.csv','rb') as trainy:
        class_reader=csv.reader(trainx,delimiter=',')
        result_reader=csv.reader(trainy,delimiter=',')
        next(class_reader)
        next(result_reader)
        i=0
        for row1,row2 in itertools.izip(class_reader,result_reader):  
            text_deleteurl = re.sub(r"http\S+","", row1[1])
            text_deletenum=re.sub("\d+","",text_deleteurl)
            text_deleteemoji=myre.sub('',text_deletenum.decode('utf8'))
            #l=list(text_deleteemoji)
            l=tuple(text_deleteemoji.lower().replace(' ',''))
            for x in range (0,len(l)-n+1):
                if(l[x:x+n] in Dicts[int(row2[1])]):
                   Dicts[int(row2[1])][l[x:x+n]]=Dicts[int(row2[1])][l[x:x+n]]+1
                else:
                   Dicts[int(row2[1])][l[x:x+n]]=1
        
                
            #f.write(row2[1])
            #f.write('\n')
            i=i+1
    #f.close()
            
    #total vocabulary

    for x in range(0,5):
        vocabulary=vocabulary+len(Dicts[x])



    for x in range(0,5):
        occur+=[0]
        occur_plus_vocabulary+=[0]
            
    for x in range(0,5):
        for key in Dicts[x]:
            occur[x]=occur[x]+Dicts[x][key]
            
    for x in range(0,5):
        occur_plus_vocabulary[x]=occur[x]+vocabulary

    #probability of each word

    for x in range(0,5):
        for key in Dicts[x]:
            Dicts[x][key]=(float(Dicts[x][key]+1))/occur_plus_vocabulary[x]



def classProbability(class_probability):
    for x in range(0,5):
        class_probability+=[0]
    with open('train_set_y.csv','rb') as trainy:
        result_reader=csv.reader(trainy,delimiter=',')
        next(result_reader)
        for row in result_reader:
            class_probability[int(row[1])]=class_probability[int(row[1])]+1;
    total=0
    for x in range(0,5):
        total=total+class_probability[x]
    for x in range(0,5):
        class_probability[x]=float(class_probability[x])/total

def tellme(Dicts,n):
        same=0
        notsame=0
        with open('test_set_x.csv','rb') as test, open('nb.csv','wb') as output, open('library_logistic_output.csv','rb') as trainy:
            output.write("Id,Category")
            output.write("\n")
            test_reader=csv.reader(test,delimiter=',')
            result_reader=csv.reader(trainy,delimiter=',')
            next(test_reader)
            next(result_reader)
            i=0
            for row1,row2 in itertools.izip(test_reader,result_reader):  
                test_probability=[]
                for x in range(0,5):
                    test_probability+=[class_probability[x]]
                text_deleteurl = re.sub(r"http\S+","", row1[1])
                text_deletenum=re.sub("\d+","",text_deleteurl)
                text_deleteemoji=myre.sub('',text_deletenum.decode('utf8'))
                l=tuple(text_deleteemoji.lower().replace(' ',''))

                for x in range(0,5):
                    for y in range (0,len(l)-n+1):
                        if(l[y:y+n] in Dicts[x]):
                            test_probability[x]=test_probability[x]*Dicts[x][l[y:y+n]]
                        else:
                            test_probability[x]=test_probability[x]/float(occur_plus_vocabulary[x])
                maxprob=0
                maxindex=0
                for x in range (0,5):
                    if(test_probability[x]>maxprob):
                        maxprob=test_probability[x]
                        maxindex=x
                if(maxindex==int(row2[1])):
                    same=same+1
                else:
                    notsame=notsame+1
                output.write(str(i))
                output.write(",")
                output.write(str(maxindex))
                output.write("\n")
                i=i+1
        print same
        print notsame
        print float(same)/(same+notsame)
paraseData_ngram(1,Dicts,occur_plus_vocabulary)
classProbability(class_probability)
tellme(Dicts,1)




