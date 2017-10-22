# comp551_project2
Machine learning project
  
 - Overview  
This is a course project for Applied Machine Learning.  
The project used TF-IDF,Ridge regression(L2-regularization) decision tree learning and bagging to classify different language class each sample sentence belongs to.  
This decision tree learning used information gain to determine priority of all possible split/creating tree node.

 - Data preprocessing
For the input training data, TF-IDF is used to convert train_set_x and test_set_x into sparse matrix with all the character they used as feature.
