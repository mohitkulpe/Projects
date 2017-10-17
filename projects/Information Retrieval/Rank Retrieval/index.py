#Python 3.0
#use time.time() on Linux

import re
import os
import collections
import time

import math
import random

from collections import defaultdict
from collections import Counter
#import other modules as needed

def main():
    """ DO NOT MODIFY.
    Main method. Constructs an Index object and runs a sample query. """
    idx = index(os.path.join('collection/'))

    print(idx.exact_query(['with', 'without', 'yemen'], 10))
    print(idx.inexact_query_champion(['with', 'without', 'yemen'], 10))
    print(idx.inexact_query_index_elimination(['with', 'without', 'yemen'], 10))
    print(idx.inexact_query_cluster_pruning(['with', 'without', 'yemen'], 10))

    print(idx.exact_query(['with', 'without', 'yemen', 'yemeni'], 10))
    print(idx.inexact_query_champion(['with', 'without', 'yemen', 'yemeni'], 10))
    print(idx.inexact_query_index_elimination(['with', 'without', 'yemen', 'yemeni'], 10))
    print(idx.inexact_query_cluster_pruning(['with', 'without', 'yemen', 'yemeni'], 10))

    print(idx.exact_query(['berlin', 'poland', 'szczecin', 'obacz', 'plane'], 10))
    print(idx.inexact_query_champion(['berlin', 'poland', 'szczecin', 'obacz', 'plane'], 10))
    print(idx.inexact_query_index_elimination(['berlin', 'poland', 'szczecin', 'obacz', 'plane'], 10))
    print(idx.inexact_query_cluster_pruning(['berlin', 'poland', 'szczecin', 'obacz', 'plane'], 10))

    print(idx.exact_query(['abc', 'pqr', 'xyz'], 10))
    print(idx.inexact_query_champion(['abc', 'pqr', 'xyz'], 10))
    print(idx.inexact_query_index_elimination(['abc', 'pqr', 'xyz'], 10))
    print(idx.inexact_query_cluster_pruning(['abc', 'pqr', 'xyz'], 10))

    print(idx.exact_query(['million', 'billion'], 10))
    print(idx.inexact_query_champion(['million', 'billion'], 10))
    print(idx.inexact_query_index_elimination(['million', 'billion'], 10))
    print(idx.inexact_query_cluster_pruning(['million', 'billion'], 10))
    # idx.print_dict()
    # idx.print_doc_list()


class index:
    def __init__(self, path):
        self.documents = {name: open(os.path.join(path, name)).read() for _, _, files in os.walk(path) for name in files
                          if name.endswith(".txt")}
        self.stopwords = open('stop-list.txt').readlines()

        self.doc_list = {}
        self.toked_docs = {}
        for docID, d in enumerate(self.documents):
            self.doc_list[docID] = d
            self.toked_docs[docID] = self.tokenize(self.documents[d])

        self.doc_freqs = self.doc_frequency(self.toked_docs)
        self.buildIndex()
        self.doc_lengths = self.doc_length(self.index)



    def buildIndex(self):
        #function to read documents from collection, tokenize and build the index with tokens
        # implement additional functionality to support methods 1 - 4
        #use unique document integer IDs

        self.index = self.build_tfidf_index(self.toked_docs, self.doc_freqs)
        self.champion_index = self.build_champion_index(self.index, 10)
        self.cluster_pruning, self.cluster_pruning_leader_index = self.build_clusterpruning_index()

         #Building TFIDF Index 
    def build_tfidf_index(self, docs, doc_freqs):
        tfidf_index = defaultdict(list)
        for docID in docs:
            doc_dict = defaultdict(list)
            for index, term in enumerate(docs[docID]):
                doc_dict[term].append(index)

            self.get_tfidf(docID, doc_dict, docs, doc_freqs, tfidf_index)

        sorted(tfidf_index.keys())
        return tfidf_index


        #Generating TFIDF Weight
    def get_tfidf(self, doc_id, term_dict, docs, doc_freqs, weight_dict):
        for word in term_dict:
            wt = (1 + math.log10(len(term_dict[word])))
            idf = math.log10(len(docs) / doc_freqs[word])

            # tf_idf_weight = wt * idf
            if len(weight_dict[word]) == 0:
                weight_dict[word].append(idf)
            weight_dict[word].append([doc_id, wt, term_dict[word]])

        return weight_dict


        #Building Champion list Index
    def build_champion_index(self, index, threshold=10):
        champion_index = defaultdict(list)
        for word in index:
            champion_index[word] = index[word] + sorted(index[word][1:], key=lambda k: k[1])[:threshold]
        return champion_index


         #Building Cluster Pruning Index
    def build_clusterpruning_index(self):
        weight_dict = defaultdict(list)

        index = set(self.toked_docs.keys())

        leaders_no = math.ceil(math.sqrt(len(index)))
        followers_no = leaders_no
        leaders = set(random.sample(index, leaders_no))
        index -= leaders

        toked_docs = {key: self.toked_docs[key] for key in leaders}
        doc_freqs = self.doc_frequency(toked_docs)
        doc_index = self.build_tfidf_index(toked_docs, doc_freqs)
        doc_lengths = self.doc_length(doc_index)

        for doc in index:
            query_vector = self.query_vector(self.toked_docs[doc])
            cosine_scores = self.cosine_search(query_vector, doc_index, doc_lengths)
            if len(cosine_scores) > 0:

                weight_dict[cosine_scores[0][0]].append(doc)

        return weight_dict, doc_index



         # Calculating Cosine Similarity
    def cosine_search(self, query_vector, index, doc_lengths):
        scores = defaultdict(lambda: 0)
        for query_term, query_wt in query_vector.items():
            if len(index[query_term]) != 0:
                idf = index[query_term][0]
                for doc_id, doc_wt, _ in index[query_term][1:]:
                    scores[doc_id] += query_wt * doc_wt * idf

        for idx in scores:
            try:
                scores[idx] /= doc_lengths[idx]
            except ZeroDivisionError:
                scores[idx] = 0

        return sorted(scores.items(), key=lambda k: k[1], reverse=True)

     
        #Generating Query Vector
    def query_vector(self, query_terms):
        query_dict = defaultdict(lambda: 0)
        for query in query_terms:
            N = len(self.documents)
            df = self.doc_freqs[query]
            try:
                query_dict[query] = math.log10(N / df)
            except ZeroDivisionError:
                query_dict[query] = 0
        return query_dict


    #Calculating Length
    def doc_length(self, index):
        my_dict = defaultdict(lambda: 0)
        for ky, big_list in index.items():
            idf = big_list[0]
            for doc_id in big_list[1:]:
                my_dict[doc_id[0]] = my_dict[doc_id[0]] + ((idf*doc_id[1]) ** 2)

        for val in my_dict:
            my_dict[val] = math.sqrt(my_dict[val])

        return my_dict


         #Calculating Document Frequency
    def doc_frequency(self, docs):
        freq_dict = Counter({})
        for doc in docs:
            freq_dict += Counter(docs[doc])

        return freq_dict

#function for exact top K retrieval (method 1)
        #Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
    def exact_query(self, query_terms, k):
        
        t1 = time.time()
        query_vector = self.query_vector(query_terms)
        cosine_scores = self.cosine_search(query_vector, self.index, self.doc_lengths)[:k]

        t2 = time.time()

        print("\nResults for the Query: ", " AND ".join(query_terms))
        print("\nExact Top K Retrieval:")
        for docID, cosine in cosine_scores:
             print(self.doc_list[docID])
        print("List Retrieved in", '{0:.10f}'.format(t2 - t1), "seconds\n")
        #return [self.doc_list[docID] for docID in result[:k]]

 
 #function for exact top K retrieval using champion list (method 2)
        #Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

    def inexact_query_champion(self, query_terms, k):
       
        t1 = time.time()
        query_vector = self.query_vector(query_terms)
        cosine_scores = self.cosine_search(query_vector, self.champion_index, self.doc_lengths)[:k]
        
        t2 = time.time()
        print("Inexact Top K Retrieval (champion List):")
        for docID, cosine in cosine_scores:
             print(self.doc_list[docID])
        print("List Retrieved in", '{0:.10f}'.format(t2 - t1), "seconds\n") 
        #return [self.doc_list[docID] for docID in result[:k]]

    
 #function for exact top K retrieval using index elimination (method 3)
        #Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

    def inexact_query_index_elimination(self, query_terms, k):
       
        t1 = time.time()

        index = {query : self.index[query] for query in query_terms}
        index = dict(sorted(index.items(), key= lambda x: x[1], reverse= True)[:int(len(query_terms)/2)])

        query_vector = self.query_vector(index.keys())
        cosine_scores = self.cosine_search(query_vector, index, self.doc_lengths)[:k]
        
        t2 = time.time()
        print("Inexact Top K Retrieval (Index Elimination):")
        for docID, cosine in cosine_scores:
             print(self.doc_list[docID])
        print("List Retrieved in", '{0:.10f}'.format(t2 - t1), "seconds\n") 
        #return [self.doc_list[docID] for docID in result[:k]]


    
#function for exact top K retrieval using cluster pruning (method 4)
        #Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
    def inexact_query_cluster_pruning(self, query_terms, k):
        
        t1 = time.time()

        query_vector = self.query_vector(query_terms)
        result = []
        cosines = self.cosine_search(query_vector, self.cluster_pruning_leader_index, self.doc_lengths)
        
        t2 = time.time()
        print("Inexact Top K Retrieval (Cluster Pruning):")
        for cosine in cosines:
            if len(result) > k:
                break
            result.append(cosine[0])
            result.extend(self.cluster_pruning[cosine[0]])
        print("List Retrieved in", '{0:.10f}'.format(t2 - t1), "seconds\n")    

        return [self.doc_list[docID] for docID in result[:k]]


    def print_dict(self):
        #function to print the terms and posting list in the index
        for token in self.index:
            print(token, [(i[0], i[2]) for i in self.index[token]])

    def print_doc_list(self):
        # function to print the documents and their document id
        for docID in self.doc_list:
            print("Doc ID: ", docID, " ==> ", self.doc_list[docID])

    def tokenize(self, document):
        return [item for item in re.findall('[\w]+', document.lower()) if item not in self.stopwords]


if __name__ == '__main__':
    main()
