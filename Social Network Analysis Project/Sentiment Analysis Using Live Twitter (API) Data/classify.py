"""
classify.py

"""

import pickle
import numpy as np
from collections import defaultdict
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from scipy.sparse import lil_matrix
import re
from sklearn.cross_validation import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from collections import Counter




def afinn_lex(terms, afinn, verbose=False):
    
    pos_words = 0
    neg_words = 0
    
    for t in terms:
        if t in afinn:
            if verbose:
                print('\t%s=%d' % (t, afinn[t]))
                
            if afinn[t] > 0:
                pos_words += afinn[t]
            else:
                neg_words += -1 * afinn[t]
                
    return pos_words,neg_words



def tokenize(text):
    return re.sub('\W+', ' ', text.lower()).split()


def pos_neg_count(tokenize,tweets,afinn):
    
    positive_count = []
    negative_count = []
    
    for token_list, tweet in zip(tokenize, tweets):
        
        pos_words, neg_words = afinn_lex(token_list, afinn)
        
        if pos_words > neg_words:
            positive_count.append((tweet['text'], pos_words, neg_words))

        elif neg_words > pos_words:
            negative_count.append((tweet['text'], pos_words, neg_words))
            
    return positive_count[0], negative_count[1]


def pos_or_neg(t, afinn):
    
    sorted_tokens = tokenize(t['text'])
    pos_words, neg_words = afinn_lex(sorted_tokens, afinn)
    
    if pos_words > neg_words:
        return 1
    
    elif neg_words > pos_words:
         return 0
    else:
        return -1
    
    
def vocabulary(tokens_list):
    vocab = defaultdict(lambda: len(vocab))
    for tl in tokens_list:
        for t in tl:
             vocab[t]
    return vocab



def csr_matrix(tokens_list, vocab,tweets):
    
    X = lil_matrix((len(tweets), len(vocab)))
    
    for i, tl in enumerate(tokens_list):
        for t in tl:
            j = vocab[t]
            X[i,j] += 1
            
    return X.tocsr()


#Cross Validation by K=480
def cross_val(b, a, nfolds):
    
    cv = KFold(len(a), nfolds)
    
    accuracies = []
    
    for train, test in cv:
        
        clf = LogisticRegression()
        
        clf.fit(b[train], a[train])
        
        pred = clf.predict(b[test])
        
        acc = accuracy_score(a[test], pred)
        
        accuracies.append(acc)
        
    avg = np.mean(accuracies)
    
    avg = round(avg, 5)
    
    return avg




def main():
    
    tweets = pickle.load(open('collected_tweets.pkl', 'rb'))
    tweets = [t for t in tweets if 'user' in t]
    url = urlopen('http://www2.compute.dtu.dk/~faan/data/AFINN.zip')
    zipfile = ZipFile(BytesIO(url.read()))
    afinn_file = zipfile.open('AFINN/AFINN-111.txt')
    
    afinn = dict()
    for line in afinn_file:
        indiviual = line.strip().split()
        if len(indiviual) == 2:
            afinn[indiviual[0].decode("utf-8")] = int(indiviual[1])
            
    tokens = [tokenize(t['text']) for t in tweets]
    
    vocab = vocabulary(tokens)
    
    a = np.array([pos_or_neg(t,afinn) for t in tweets])
    b = csr_matrix(tokens, vocab, tweets)
    c = np.zeros(len(tweets))
    d = np.ones(len(vocab))
    
    
    for i in range(len(tweets)):
        for j in range(b.indptr[i], b.indptr[i + 1]):
            colidx = b.indices[j]
            c[i] += d[colidx] * b.data[j]

    print('Accuracy of Classifier:', cross_val(b, a, 480))
    # 0.87639
    
    
    
    for a1,a2 in Counter(a).items():
        
        if a1>=0:
            res1 = a2

        else:
            res2 = a2
            
    pickle.dump(res2, open('classifier.pkl', 'wb'))
   
   
    pos_count=[]
    neg_count=[]
    
    cnt = pos_neg_count(tokens, tweets, afinn)
    
    pos_count.append(cnt[0])
    neg_count.append(cnt[1])

    pickle.dump((res1, res2, pos_count, neg_count), open('classifier.pkl', 'wb'))



if __name__ == '__main__':
    main()
    
    
#Reference: http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010
