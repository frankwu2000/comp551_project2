# comp551_project2
Machine learning project
  
 - Overview  
This is a course project for Applied Machine Learning.  
The project used TF-IDF,Ridge regression(L2-regularization), decision tree learning and bagging(kinda) to classify different language class each sample sentence belongs to.  
This decision tree learning used information gain to determine priority of all possible split/creating tree node.

- File structure  
  - "data_set" : the "data_set" folder contains all given training data and test data. 
    - Due to restriction of my computer memory, I split the training data set and put them in the "split_train_set" folder so I can run the decision tree respectively on each split sample.
  - "output_data_set" : the output_data_set folder contains all output data created by decision tree. "output_data_split" contains all outcomes created by smaller decision tree trained by split data sample from above. Then I average the split result to get an overall result.
  - "split_train_set" and "output_file_combine.py" are python scripts that one splits the data set to smaller size and one concludes the split sample output to an overall average orespectively.
  - "decision_tree.py","decision_tree2.py","decision_tree3.py" and "decision_tree4.py" are just to run the sample more efficiently. (it still takes about 10 hours to run all sample data (about 278000 training samples))

- Running file  
   with given training_x.csv , training_y.csv and test_x.csv, go to file "decision_tree.py" line 326   
   ```
   train_decision_tree(arg1, arg2, arg3, arg4)  
   ```
   arg1: input training x data filename (csv type)  
   arg2: input training y data  filename (csv type)  
   arg3: input test x data  filename (csv type)  
   arg4: output predict y data filename (csv type)  
 
   then run   
   ```
   python decision_tree.py  
   ```  
 

- Data preprocessing

  For the input training data, TF-IDF is used to convert train_set_x and test_set_x into sparse matrix with every character in the sample documents as features. Ridge regression is also used for training data to reduce number of features.

- Decision tree 

  The decision tree expand node based on information gain used entropy of each set. I first preprocess all possible split point for each feature by calculating the midpoint of all training x value. Then use information gain to pick the split with gratest information gain. The tree keeps expanding until the information gain is smaller than the predefined threshold or it used all features.  
  
  NOTE: threshold and max_feature_num are input parameter when initalizing decision tree class.
    - threshold is the smallest information gain allowed to grow the tree.   
    - max_feature_num is the maximum depth allowed to grow the tree.
  
- Conclusion

   The outcome is not ideal since it only get 0.59 accuracy on the given test set. 
 Still need to improve the algorithm.

