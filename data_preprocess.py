import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer 
import csv
import re

from sklearn.linear_model import LogisticRegression
#from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
#from sklearn.naive_bayes import MultinomialNB
from scipy.sparse import *

train_x = []
train_y = []
test_x = []

with open("data_set/train_set_x.csv","rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader,None) #skip header of file
    for row in reader:
        text_deleteurl = re.sub(r"http\S+","", row[1])
        text_deletenum=re.sub("\d+","",text_deleteurl)
        l=text_deletenum.replace(" ","").lower()
        train_x.append(l)

with open("data_set/train_set_y.csv","rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader,None) #skip header of file
    for row in reader:
        train_y.append(row[1])
        
with open("data_set/test_set_x.csv","rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader,None) #skip header of file
    for row in reader:
        text_deletenum=re.sub("\d+","",row[1])
        l=text_deletenum.replace(" ","").lower()
        test_x.append(l)
        
vec = TfidfVectorizer(decode_error='strict',analyzer='char',min_df=0)
train_x=vec.fit_transform(train_x)
features = vec.get_feature_names()

vec2 = TfidfVectorizer(decode_error='strict',analyzer='char',min_df=0,vocabulary=features)
test_x = vec2.fit_transform(test_x)
#print(test_x)


#print("train_x is a matrix with size : ",train_x.shape[0],train_x.shape[1])
#print("train_y is an array with size: ",len(train_y))

lr_classifier = LogisticRegression(penalty='l2', C=1)
lr_classifier.fit(train_x, train_y)

test_y_pred = lr_classifier.predict(test_x)

test_y_pred_temp = test_y_pred.tolist()

with open("library_logistic_output.csv",'wb') as output:
    output.write("Id,Category")
    output.write("\n")
    for i in range(len(test_y_pred_temp)):
        output.write(str(i))
        output.write(",")
        output.write(test_y_pred_temp[i])
        output.write("\n")





