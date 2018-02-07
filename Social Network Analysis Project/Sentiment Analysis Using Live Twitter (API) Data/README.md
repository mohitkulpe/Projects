# Sentiment Analysis Using Twitter Live Data

This Project will do a more open-ended exploration of online social networking.

Here is what each script do:

- collect.py: 
           Main objective of collect.py is to gather (collect) data. I have used twitter API to collect data, this python script takes control of twitter API by passing Consumer Token & sceret key using get_twitter() method for establishing a twitter connection. Now here I am Collecting  tweets with search/tweets function by using keyword 'h1b' & limiting it by 1000 with max_id. After collecting data (tweets) I saved it in collected_tweets.pkl. In addition to that I generated text file named network.txt in which I have saved user ids based on the screen names whose user profile is not protected, this file will be used for creating clusters (Communities). 


- 'cluster.py:
           Main objective of cluster.py is to create clusters. This python script imports network.txt & clusters users based on the screen names and ids. First it creates a graph with  edges as the screen names and id & then it takes the connected components of the subgraph. This subgraph is done by using girvan_newman algorithm. After creating subgraphs this script saves the list of divided components to the pickle file named 'clusters.pkl'.


- classify.py:
           Main objective of classify.py is to classify data into different classes. This python script imports data from the clusters.pkl also it takes positive & negative data from the AFINN. Tweets are first strip using tokenize function. After that positive & negative counts are retrieved then converting that tweet into positive or negative by comparing positive counts with negative counts. Then vocab is created by using vocabulary function then converting vocab into CSR Matrix. Then cross validation is done by using kfold method to find accuracy of classifier, here I have used Logistic Regression classifier. In this assignment I tried to classify tweets based on who supports 'h1b' and who not using positive & negative words.


- summarize.py:
             Main objective of summarize.py is to display the result of overall assignment. This python script imports 'collected_tweets.pkl', 'clusters.pkl' and 'classifier.pkl' from which tweet related information is extracted from 'collected_tweets.pkl', Communities related information is extracted from 'clusters.pkl' and Classification related information is extracted from 'classifier.pkl'.

  - Number of users collected:
  - Number of messages collected:
  - Number of communities discovered:
  - Average number of users per community:
  - Number of instances per class found:
  - One example from each class:
  
  # Data from Affin Library
