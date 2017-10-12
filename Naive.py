import csv
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')
prase_data=[];
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    
    
f=open('myfile.txt','w')
with open('data_set/train_set_x.csv','rb') as csvfile:
     classreader=csv.reader(csvfile,delimiter=',')
     for row in classreader:
         text_deleteurl = re.sub(r"http\S+","", row[1])
         text_deletenum=re.sub("\d+","",text_deleteurl)
         text_deleteemoji=emoji_pattern.sub(r'',text_deletenum).replace(" ","")
         l=list(text_deleteemoji)
         for c in l:
             if(c!=' '):f.write(c.lower()+" ")
         f.write('\n')
f.close()

