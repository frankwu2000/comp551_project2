#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

char_set =set()

f=open("newfile.txt","w") 
with open("data_set/train_set_x.csv",'rb') as csvfile:
    reader = csv.reader(csvfile,delimiter=',')
    next(reader,None) #skip header of file
    for row in reader:
        text_deleteurl = re.sub(r"http\S+","", row[1])
        text_deletenum=re.sub("\d+","",text_deleteurl)
        l=list(text_deletenum)
        for c in l:
            if(c!=' '):f.write(c.lower()+" ")
        f.write('\n')
f.close()
