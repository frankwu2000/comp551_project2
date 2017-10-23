import sklearn
import csv
import re
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.linear_model import LogisticRegression
import math
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
import numpy as np


#load two train data files, one test data file, and formatting them
def load_dataset(train_x_param, train_y_param, test_x_param):
    train_x_raw = []
    train_y_raw = []
    test_x_raw =[]
    with open(train_x_param,"r",encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) #skip header of file
        for row in reader:
            # text_deleteurl = re.sub(r"http\S+","", row[1])
            # text_deletenum=re.sub("\d+","",text_deleteurl)
            # l=text_deletenum.replace(" ","").lower()
            l=row[1].replace(" ","").lower()
            train_x_raw.append(l)

    with open(train_y_param,"r",encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) #skip header of file
        for row in reader:
            train_y_raw.append(row[1])
        
    with open(test_x_param,"r",encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) #skip header of file
        for row in reader:
            # text_deletenum=re.sub("\d+","",row[1])
            # l=text_deletenum.replace(" ","").lower()
            l=row[1].replace(" ","").lower()
            test_x_raw.append(l)

    return train_x_raw,train_y_raw,test_x_raw

#tfidf preprocessing - convert train_x_raw and test_x_raw to sparse matrix with size of (num_documents,num_features) 
def tfidf_preprocess(train_x_raw,train_y_raw,test_x_raw):
    #print("start tfidf and svc data preprocessing...")    
    

    vec = TfidfVectorizer(decode_error='strict',analyzer='char',dtype=np.float32)
    train_x=vec.fit_transform(train_x_raw)

    # features = vec.get_feature_names()
    # print(dict(zip(features,vec.idf_)))
    # new_features = features[0:220]
    # print(new_features)
    # lsvc = LinearSVC(C=0.01, penalty="l2", dual=False).fit(train_x, train_y_raw)
    # model = SelectFromModel(lsvc, prefit=True)

    # train_x = model.transform(train_x)
   
    print("train_x shape: ",train_x.shape)
    # print("number of features: ",len(features))
    # print("\nfeatures: ",features)
    
    # vec_less_features = TfidfVectorizer(decode_error='strict',analyzer='char',min_df=0,vocabulary=new_features)
    # train_x=vec_less_features.fit_transform(train_x_raw)
     
    vec2 = TfidfVectorizer(decode_error='strict',analyzer='char',vocabulary=vec.get_feature_names(),dtype=np.float32)
    test_x = vec2.fit_transform(test_x_raw)
    # test_x = model.transform(test_x)
    #print("test_x shape: ",test_x.shape)
    # test_x = vec_less_features.fit_transform(test_x_raw)
    #print(test_x)
    #print("train_x is a matrix with size : ",train_x.shape[0],train_x.shape[1])
    #print("train_y is an array with size: ",len(train_y))
    return train_x,test_x


       
# Library function : logistic classification    
def logistic_classification(train_x,train_y,test_x,output_filename):
    lr_classifier = LogisticRegression(penalty='l2', C=1)
    lr_classifier.fit(train_x, train_y)
    # predict on the test file
    test_y_pred = lr_classifier.predict(test_x)
    test_y_pred_temp = test_y_pred.tolist()

    # write the output to the output file
    with open(output_filename,'w') as output:
        output.write("Id,Category")
        output.write("\n")
        for i in range(len(test_y_pred_temp)):
            output.write(str(i))
            output.write(",")
            output.write(test_y_pred_temp[i])
            output.write("\n")
    print("output logistic complete")

library_logisitic("data_set/train_set_x.csv","data_set/train_set_y.csv","data_set/test_set_x.csv","output_data_set/logistic_predict_feature_selection.csv")
