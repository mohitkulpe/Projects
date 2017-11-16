# coding: utf-8

#  Movie Ratings Prediction

from collections import Counter, defaultdict
import math
import numpy as np
import os
import pandas as pd
import re
from scipy.sparse import csr_matrix
import urllib.request
import zipfile

def download_data():
    """ Download and unzip data.
    """
   
    zfile = zipfile.ZipFile('ml-latest-small.zip')
    zfile.extractall()
    zfile.close()


def tokenize_string(my_string):
    """ You should use this in your tokenize function.
    """
    return re.findall('[\w\-]+', my_string.lower())


def tokenize(movies):
    """
    Append a new column to the movies DataFrame with header 'tokens'.
    This will contain a list of strings, one per token, extracted
    from the 'genre' field of each movie. Use the tokenize_string method above.
    
    """
    
    
    movie_t = []

    rang_m =  (len(movies))
    
    for g in range(0,rang_m):
        g1 = movies['genres'][g]
    
    
        ts = tokenize_string(g1)
   
        movie_t.append(ts)
    
    
   

    movies['tokens'] = movie_t
    
    
    return movies
    
    pass


def featurize(movies):
    """
    Append a new column to the movies DataFrame with header 'features'.
    Each row will contain a csr_matrix of shape (1, num_features). Each
    entry in this matrix will contain the tf-idf value of the term, as
    defined in class:
    tfidf(i, d) := tf(i, d) / max_k tf(k, d) * log10(N/df(i))
    where:
    i is a term
    d is a document (movie)
    tf(i, d) is the frequency of term i in document d
    max_k tf(k, d) is the maximum frequency of any term in document d
    N is the number of documents (movies)
    df(i) is the number of unique documents containing term i
    
    """
        
    token_list = []

    t_m_dict = defaultdict(list)
    
    vocab = defaultdict(lambda: 0)
    
    
    for t1 in movies['tokens']:
        for t2 in t1:
            token_list.append(t2)
   
    
    t_count = Counter(token_list)
   
    
    tc = 0
    sorted_t_count = sorted(t_count.items())
    
    
    for tc1, val in sorted_t_count:
        vocab[tc1] += tc
        tc += 1
    
        
    rang_m =  (len(movies))
    
    for j in range(0,rang_m):
        
        for t3 in movies['tokens'][j]:
            t_m_dict[t3].append(movies.title[j])
  
    
   
    csr_mat = []

    for t4 in movies['tokens']:
       
        
        r = 0
        tfidf_res = []
        row = []
        col = []
    
        g_count = Counter(sorted(t4))
        
        
        for t5 in sorted(t4):
            col.append(vocab[t5])
         
            row.append(r)
          
            
            tf_ij = g_count[t5]
            
            
            max_fq = max(g_count.values())
            
    
            
            for t6, val in (t_m_dict.items()):
                if t6 == t5:
                    df_i = len(val)
                    
                
          
                
            N = len(movies)
           
            
            
            tf = ((tf_ij)/max_fq)
            
            idf = (np.log10(N/df_i))
        
        
            tf_idf = (tf*idf)
            
            tfidf_res.append(tf_idf)
            
           
                
        
        X = csr_matrix((tfidf_res,(row, col)),shape=(1,len(t_count.keys())))
     
        csr_mat.append(X)
    
        
    movies['features'] = csr_mat
    
    tup = (movies,vocab)
   
    
    return tup
    
       
    pass


def train_test_split(ratings):
    """
    Returns a random split of the ratings matrix into a training and testing set.
    """
    test = set(range(len(ratings))[::1000])
    train = sorted(set(range(len(ratings))) - test)
    test = sorted(test)
    return ratings.iloc[train], ratings.iloc[test]


def cosine_sim(a, b):
    """
    Compute the cosine similarity between two 1-d csr_matrices.
    Each matrix represents the tf-idf feature vector of a movie.
   
      The cosine similarity, defined as: dot(a, b) / ||a|| * ||b||
      where ||a|| indicates the Euclidean norm (aka L2 norm) of vector a.
    """
    
    
   
    x = (a.dot(b.transpose()))
    
    y = (np.sqrt(a*a.transpose())*np.sqrt(b*b.transpose()))
    
    res = (x/y).tolist()[0][0]
   
    
    return res
    

    pass


def make_predictions(movies, ratings_train, ratings_test):
    """
    Using the ratings in ratings_train, predict the ratings for each
    row in ratings_test.
    To predict the rating of user u for movie i: Compute the weighted average
    rating for every other movie that u has rated.  Restrict this weighted
    average to movies that have a positive cosine similarity with movie
    i. The weight for movie m corresponds to the cosine similarity between m
    and i.
    If there are no other movies with positive cosine similarity to use in the
    prediction, use the mean rating of the target user in ratings_train as the
    prediction.
    
    """
  
    
    prediction_list = []

    common_rating = []

    for r_test in ratings_test.itertuples():
        
      
        
        
        a = ((movies[movies.movieId == r_test.movieId]).features.values[0])
        
       
        
        cos_list = []
        rating_prod = []
        
        for r_train in ratings_train.itertuples():
           
            
            if r_test.userId == r_train.userId :
                
                b = ((movies[movies.movieId == r_train.movieId]).features.values[0])
                
               
                
                cos = cosine_sim(a, b)
                
               
                cos_list.append(cos)
                
                
                ratings = ((ratings_train[ratings_train.movieId == r_train.movieId]).rating.values[0])
              
                
                common_rating.append(ratings)
                
                prod = (cos*ratings)              
                rating_prod.append(prod)
                               
                
        
        
        sum_cos_list = sum(cos_list)

        sum_rating_prod = sum(rating_prod)
            
            
        if (sum_cos_list)>0:
            
            wt_avg = (sum_rating_prod/sum_cos_list)
            
            prediction_list.append(wt_avg)
            
        else:
            
            wt_avg = (np.mean(common_rating))
            
            prediction_list.append(wt_avg)
            
    prediction = np.array(prediction_list)   
           
    
    return prediction
                
    pass


def mean_absolute_error(predictions, ratings_test):
    """
    Return the mean absolute error of the predictions.
    """
    return np.abs(predictions - np.array(ratings_test.rating)).mean()


def main():
    download_data()
    path = 'ml-latest-small'
    ratings = pd.read_csv(path + os.path.sep + 'ratings.csv')
    movies = pd.read_csv(path + os.path.sep + 'movies.csv')
    movies = tokenize(movies)
    movies, vocab = featurize(movies)
    print('vocab:')
    print(sorted(vocab.items())[:10])
    ratings_train, ratings_test = train_test_split(ratings)
    print('%d training ratings; %d testing ratings' % (len(ratings_train), len(ratings_test)))
    predictions = make_predictions(movies, ratings_train, ratings_test)
    print('error=%f' % mean_absolute_error(predictions, ratings_test))
    print('Top 10 Rating Predictions:')
    print(predictions[:10])


if __name__ == '__main__':
    main()

