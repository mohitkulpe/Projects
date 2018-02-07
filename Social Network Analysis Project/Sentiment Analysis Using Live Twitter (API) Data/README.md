# Sentiment Analysis Using Twitter Live Data

This Project will do a more open-ended exploration of online social networking.

Here is what each script do:

- `collect.py`: This should collect data used in your analysis. This may mean submitting queries to Twitter or Facebook API, or scraping webpages. The data should be raw and come directly from the original source -- that is, you may not use data that others have already collected and processed for you (e.g., you may not use [SNAP](http://snap.stanford.edu/data/index.html) datasets). Running this script should create a file or files containing the data that you need for the subsequent phases of analysis.

- `cluster.py`: This should read the data collected in the previous steps and use any community detection algorithm to cluster users into communities. You may write any files you need to save the results.

- `classify.py`: This should classify your data along any dimension of your choosing (e.g., sentiment, gender, spam, etc.). You may write any files you need to save the results.

- `summarize.py`: This should read the output of the previous methods to write a textfile called `summary.txt` containing the following entries:
  - Number of users collected:
  - Number of messages collected:
  - Number of communities discovered:
  - Average number of users per community:
  - Number of instances per class found:
  - One example from each class:
  
  # Data from Affin Library
