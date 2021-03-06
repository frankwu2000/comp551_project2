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
    lsvc = LinearSVC(C=0.01, penalty="l2", dual=False).fit(train_x, train_y_raw)
    model = SelectFromModel(lsvc, prefit=True)

    train_x = model.transform(train_x)
   
    print("train_x shape: ",train_x.shape)
    # print("number of features: ",len(features))
    # print("\nfeatures: ",features)
    
    # vec_less_features = TfidfVectorizer(decode_error='strict',analyzer='char',min_df=0,vocabulary=new_features)
    # train_x=vec_less_features.fit_transform(train_x_raw)
    
    vec2 = TfidfVectorizer(decode_error='strict',analyzer='char',vocabulary=vec.get_feature_names(),dtype=np.float32)
    test_x = vec2.fit_transform(test_x_raw)
    test_x = model.transform(test_x)
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


    
#--------------------------------------------------------------------------------------------------------
# Decision tree node
class Node:
    pos_child = None
    neg_child = None
    split_value = None
    def __init__(self,x_set,findex):
        self.x_set = x_set
        self.findex = findex
        


# Decision Tree
class Decision_tree:
    featured_split_values = {}

    def __init__(self,threshold,max_feature_index,train_x,train_y):
        self.threshold = threshold
        self.max_feature_index = max_feature_index
        self.train_x = train_x
        self.train_y = train_y
        
    def build_tree(self,cur_node):

        if cur_node.findex > self.max_feature_index:
            return cur_node
        
        childs_set,information_gain,best_split_value = self.split_node(cur_node.findex,cur_node.x_set)
        cur_node.split_value = best_split_value
        
        if information_gain < self.threshold:
            return cur_node
        cur_node.pos_child = Node(childs_set[0],cur_node.findex+1)
        cur_node.neg_child = Node(childs_set[1],cur_node.findex+1)
        self.build_tree(cur_node.pos_child)
        self.build_tree(cur_node.neg_child)
        return cur_node
    
    def predict_y(self,root,test_x):
        predict_y = []
        for row in range(test_x.shape[0]):
            cur_node = root
            for column in range(test_x.shape[1]):
                if test_x[row,column] >= cur_node.split_value:
                    if cur_node.pos_child:
                        cur_node = cur_node.pos_child
                else:
                    if cur_node.neg_child:
                        cur_node = cur_node.neg_child
            predict_y.append(self.get_best_y(cur_node.x_set))
        return predict_y
    
    def get_best_y(self,x_set):
        best_len = -1
        best_key = -1
        for key in x_set.keys():
            if len(x_set[key]) > best_len:
                best_len = len(x_set[key])
                best_key = key
        return best_key
    
# help function to build tree
    
    #match sparse_matrix train_x and list train_y
    #combine to be a dictionary with form:
    #xy_set: {
    #[class 0:[0,1,2,3,4]]
    #[class 1:[5,6,7]]
    #[class 2:[8,9,10]]
    #[class 4:[11,12,13,14,15]]}
    #where element is the documentID in train_x
    
    def combine_set(self):
        xy_dic = {}
        for i in range(len(self.train_y)):
            if self.train_y[i] not in xy_dic:
                xy_dic[self.train_y[i]]=[i]
            else:
                xy_dic[self.train_y[i]].append(i)
        return xy_dic

    #create positive children set and negative children set from a xy_set using split_value and split feature index
    def create_child(self,parent_set,split_value,splitfeature_index):
        pos_set = {}
        neg_set = {}
        for key in parent_set.keys():
            for i in parent_set[key]:
                if self.train_x[i,splitfeature_index] >= split_value:
                    if key not in pos_set:
                        pos_set[key]=[i]
                    else:
                        pos_set[key].append(i)
                else:
                    if key not in neg_set:
                        neg_set[key]=[i]
                    else:
                        neg_set[key].append(i)
        return [pos_set,neg_set]

    
    def entropy(self,xy_dic):
        total_entropy = 0
        total_count_set = self.get_sum_dict(xy_dic)
        for key in xy_dic.keys():
            total_entropy -= len(xy_dic[key])/total_count_set * math.log(len(xy_dic[key])/total_count_set,2)
        return total_entropy

    def information_gain(self,parent_set, split_value, splitfeature_index):
        children = self.create_child(parent_set,split_value,splitfeature_index)
        child0count = self.get_sum_dict(children[0])
        child1count = self.get_sum_dict(children[1])
        totalcount = child0count + child1count
        return children , self.entropy(parent_set) - child0count/totalcount*self.entropy(children[0]) - child1count/totalcount*self.entropy(children[1])

    def split_node(self,findex,parent_set):
        
        best_info_gain = -10000
        best_split_value = 0
        split_value_to_children_dic = {}
        best_children = []
        for split_value in self.featured_split_values[findex]:
            children,temp = self.information_gain(parent_set,split_value,findex)
            if temp > best_info_gain:
                best_info_gain = temp
                best_split_value = split_value
                best_children = children
        return best_children,best_info_gain,best_split_value
    
    def get_sum_dict(self,x_set):
        sum = 0
        for key in x_set.keys():
            sum += len(x_set[key])
        return sum
            
    def preprocess_possible_split(self):
        featured_columns = {}
        for column in range(self.train_x.shape[1]):
            for row in range(self.train_x.shape[0]):
                if column not in featured_columns:
                    featured_columns[column] = []
                else:
                    featured_columns[column].append(self.train_x[row,column])

        
        featured_split_values =featured_columns
        #get featured column to a list
        for findex in featured_split_values.keys():
            featured_list = sorted(featured_columns[findex])
            split_values=[]
            for i in range(len(featured_list)):
                if i-1 >= 0 :
                    if featured_list[i-1]!=0 and featured_list[i]!=0:
                        split_values.append((featured_list[i-1]+featured_list[i])/2)
            featured_split_values[findex]=split_values     
        self.featured_split_values = featured_split_values
#--------------------------------------------------------------------------------------------------------
def train_accuracy(predict_y,train_y):
    correct=0
    for i in range(len(predict_y)):
        if predict_y[i] == train_y[i]:
            correct += 1
    return correct/len(predict_y)

def output_predict_to_file(predict_y,output_filename):
    with open(output_filename,"w",encoding='UTF8') as output:
        output.write("Id,Category")
        output.write("\n")
        for i in range(len(predict_y)):
            output.write(str(i))
            output.write(",")
            output.write(predict_y[i])
            output.write("\n")
    print("output file complete")
            
#-----------start runing-----------------------------
def train_decision_tree(train_x_param,train_y_param,test_x_param,output_filename):
    #print("start running...")
    train_x_raw,train_y_raw,test_x_raw = load_dataset(train_x_param,train_y_param,test_x_param)

    #Prepreocess the training set and test set
    train_x,test_x=tfidf_preprocess(train_x_raw,train_y_raw,test_x_raw)

    #Library function: logistic 
    # logistic_classification(train_x,train_y_raw,test_x,"output_data_set/library_logistic_output.csv")

    #-----------decision tree-----------------------------
    #print("Initialize the decision tree...")
    #preprocess featured columns


    #Initialize the decision tree
    dt = Decision_tree(0.0001,train_x.shape[1]-1,train_x,train_y_raw)
    dt.preprocess_possible_split()

    root=Node(dt.combine_set(),0)

    #Start building/training the tree
    print("start building tree...")
    dt.build_tree(root)

    #Start predicting the test set
    print("finish building tree, start predicting y...")
    predict_y_values=dt.predict_y(root,test_x)
    # predict_y_values=dt.predict_y(root,train_x)

    #Output the result to csv file
    #print("finish predicting y, start output result to file...")
    output_predict_to_file(predict_y_values,output_filename)
    # print("train accuracy: ",train_accuracy(predict_y_values,train_y))

#train_decision_tree("data_set/train_set_x.csv","data_set/train_set_y.csv","data_set/test_set_x.csv","output_data_set/decision_tree_predict.csv")

x_trainset_list =[]
y_trainset_list =[]
output_file_list=[]

for i in range(50,80):
    x_trainset_list.append("data_set/split_train_set/train_set_x_" + str(i) +".csv")
    y_trainset_list.append("data_set/split_train_set/train_set_y_" + str(i) +".csv")
    output_file_list.append("output_data_set/output_data_set_split/decision_tree_output_" + str(i) +".csv")


for i in range(len(output_file_list)):
    print("process file "+str(i))
    train_decision_tree(x_trainset_list[i],y_trainset_list[i],"data_set/test_set_x.csv",output_file_list[i])



