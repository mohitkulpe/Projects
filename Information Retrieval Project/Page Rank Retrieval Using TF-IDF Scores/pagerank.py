# Python 3.0
#use time.time() on Linux

import re
import os
import collections
import time
import numpy as np
#import other modules as needed

alpha = 0.15
EPS = 1E-3

def powerVector(AM, previous_p_rank):
    while True:
        rank = np.matmul(previous_p_rank, AM)
        if np.linalg.norm(previous_p_rank - rank) < EPS: return rank
        previous_p_rank = rank


def page_rank(mat, k):
    #function to implement pagerank algorithm
    #input_file - input file that follows the format provided in the assignment description


    """
    N, _ = mat.shape
    for i, row in enumerate(mat):
        no_of_1 = np.count_nonzero(row)
        for j, value in enumerate(row):
            if no_of_1:
                mat[i][j] = 1/N
            else:
                mat[i][j] = alpha/N if value == 0 else (1 - alpha) / no_of_1 
                + (alpha / N)
                
                """


# Generating Initial Page Rank Iteration
    N, _ = mat.shape
    for i, row in enumerate(mat):
        no_of_1 = np.count_nonzero(row)
        for j, value in enumerate(row):
            if no_of_1:
                mat[i][j] = alpha/N if value == 0 else (1 - alpha) / no_of_1 + (alpha / N)
            else:
                mat[i][j] = 1/N



# Generating Power Vector
    p_rank = powerVector(mat, np.array([alpha for i in range(N)]))
    #print(p_rank)
   # return sorted(range(len(p_rank)), key=lambda x: p_rank[x])[:k]

    p_rank = {i: k for i, k in enumerate(p_rank)}
    return sorted(p_rank.items(), key=lambda x:x[1])[:k]
    #print(p_rank)



# Reading Input Files

input_file = ["test1.txt", "test2.txt"]
#input_file = [endswith(".txt")]
for file_name in input_file:
    print("\nPage Ranks of Documents in Input File '",file_name,"' with Teleportation rate α = 0.15")
    print("\nDocument List according to their Page Rank:")
    print("\nDocuments  Page Rank")
    print("---------  ---------------")

    
    with open(file_name) as file:

        # Read number of nodes
        node = int(file.readline())

        # Read number of links
        link = int(file.readline())

       
        Matrix = np.zeros((node, node), dtype=np.float64)
        for x in file:
            a, b = map(int, x.split())
            Matrix[a][b] = 1




    p_rank = page_rank(Matrix, 10)
        # t1 = time.time()

# Printing Top 10 documents ID with page rank
    for doc, score in p_rank:
        print("Doc", doc,"    ", score)
        # print("Page Ranks Generated in", '{0:.10f}'.format(t2 - t1), "seconds\n")
    print("\n")
    
   