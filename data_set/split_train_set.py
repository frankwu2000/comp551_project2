import csv
import re

#load two train data files, one test data file, and formatting them
def load_dataset(train_x_param, train_y_param):
    train_x_raw = []
    train_y_raw = []
    with open(train_x_param,"r",encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) #skip header of file
        for row in reader:
            text_deleteurl = re.sub(r"http\S+","", row[1])
            text_deletenum=re.sub("\d+","",text_deleteurl)
            l=text_deletenum.replace(" ","").lower()
            train_x_raw.append(l)

    with open(train_y_param,"r",encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) #skip header of file
        for row in reader:
            train_y_raw.append(row[1])
  
    return train_x_raw,train_y_raw,

def split_train_set(train_x_raw,train_y_raw):
    train_x_list=[]
    train_y_list=[]
    i = 0
    j = i+2750
    while i < len(train_x_raw) and j < len(train_y_raw):
        train_x_list.append(train_x_raw[i:j])
        train_y_list.append(train_y_raw[i:j])
        i=i+2750
        j=j+2750
    train_x_list.append(train_x_raw[i:len(train_x_raw)])
    train_y_list.append(train_y_raw[i:len(train_y_raw)])
    return train_x_list,train_y_list

def output_filename_generate(train_x_list):
    output_x_filenames=[]
    output_y_filenames=[]
    for i in range(len(train_x_list)):
        output_x_fname="split_train_set/train_set_x_"
        output_x_fname += str(i)
        output_x_fname += '.csv'
        output_x_filenames.append(output_x_fname)

        output_y_fname="split_train_set/train_set_y_"
        output_y_fname += str(i)
        output_y_fname += '.csv'
        output_y_filenames.append(output_y_fname)
    return output_x_filenames,output_y_filenames

def output_file_generate(output_x_filenames,output_y_filenames,train_x_list,train_y_list):
    for findex in range(len(output_x_filenames)):
        with open(output_x_filenames[findex],"w",encoding="UTF8") as output:
            output.write("Id,Category")
            output.write("\n")
            for i in range(len(train_x_list[findex])):
                output.write(str(i))
                output.write(",")
                output.write(train_x_list[findex][i])
                output.write("\n")    
            

    for findex in range(len(output_y_filenames)):
        with open(output_y_filenames[findex],"w",encoding="UTF8") as output:
            output.write("Id,Category")
            output.write("\n")
            for i in range(len(train_y_list[findex])):
                output.write(str(i))
                output.write(",")
                output.write(train_y_list[findex][i])
                output.write("\n")    
     
train_x_raw,train_y_raw = load_dataset("train_set_x.csv","train_set_y.csv")
train_x_list,train_y_list = split_train_set(train_x_raw,train_y_raw)
output_x_filenames,output_y_filenames = output_filename_generate(train_x_list)

output_file_generate(output_x_filenames,output_y_filenames,train_x_list,train_y_list)

x_trainset_list =[]
y_trainset_list =[]
output_file_list=[]

for i in range(2,25):
    x_trainset_list.append("data_set/split_train_set/train_set_x_" + str(i) +".csv")
    y_trainset_list.append("data_set/split_train_set/train_set_y_" + str(i) +".csv")
    output_file_list.append("output_data_set/output_data_set_split/decision_tree_output_" + str(i) +".csv")

# for i in range(25,50):
#     x_trainset_list.append("data_set/split_train_set/train_set_x_" + str(i) +".csv")
#     y_trainset_list.append("data_set/split_train_set/train_set_y_" + str(i) +".csv")
#     output_file_list.append("output_data_set/output_data_set_split/decision_tree_output_" + str(i) +".csv")

# for i in range(50,75):
#     x_trainset_list.append("data_set/split_train_set/train_set_x_" + str(i) +".csv")
#     y_trainset_list.append("data_set/split_train_set/train_set_y_" + str(i) +".csv")
#     output_file_list.append("output_data_set/output_data_set_split/decision_tree_output_" + str(i) +".csv")

# for i in range(75,101):
#     x_trainset_list.append("data_set/split_train_set/train_set_x_" + str(i) +".csv")
#     y_trainset_list.append("data_set/split_train_set/train_set_y_" + str(i) +".csv")
#     output_file_list.append("output_data_set/output_data_set_split/decision_tree_output_" + str(i) +".csv")

#print(x_trainset_list)


