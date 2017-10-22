import csv
def combine_output_file(num_split_file):
    predict_y_dlist = []
    predict_ys=[]
    file_name = "output_data_set/output_data_set_split/decision_tree_output_"
    for i in range(num_split_file):
        with open(file_name+str(i)+".csv","r",encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            for line in reader:
                if int(line[0])>len(predict_y_dlist)-1:
                    temp_dic={}
                    temp_dic[int(line[1])]=1
                    predict_y_dlist.append(temp_dic)
                elif int(line[1]) not in predict_y_dlist[int(line[0])]:
                    predict_y_dlist[int(line[0])][int(line[1])]=1
                else:    
                    predict_y_dlist[int(line[0])][int(line[1])]+=1

    for elem in predict_y_dlist:
    	best_key = -1
    	best_key_len = -1
    	for key in elem.keys():
    		if elem[key] > best_key_len:
    			best_key = key
    			best_key_len = elem[key]
    	predict_ys.append(best_key)
    return predict_ys

def output_predict_to_file(predict_y,output_filename):
    with open(output_filename,"w",encoding='UTF8') as output:
        output.write("Id,Category")
        output.write("\n")
        for i in range(len(predict_y)):
            output.write(str(i))
            output.write(",")
            output.write(str(predict_y[i]))
            output.write("\n")
    print("output file complete")

output_predict_to_file(combine_output_file(101),"output_data_set/decision_tree_output_with_split2.csv")

            