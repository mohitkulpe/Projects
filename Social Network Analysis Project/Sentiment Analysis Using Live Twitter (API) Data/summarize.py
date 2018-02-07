"""
sumarize.py
"""

import pickle


def main():
    
    tweets = pickle.load(open('collected_tweets.pkl', 'rb'))
    clus = pickle.load(open('clusters.pkl', 'rb'))
    
    i = 0
    clus_len = []
    tweet_text = []
    
    for i in range(len(clus)):
        for j in range(0, 2):
            clus_len.append(len(clus[i][j]))
            
    for t in tweets:
        tweet_text.append(t['text'])
        
        
    screenname_list = []
    
    for t1 in tweets:
        if t1['user']['protected'] == False:
            screenname_list.append(t1['user']['screen_name'])
            
            
    clf = pickle.load(open('classifier.pkl', 'rb'))

    f = open('summary.txt', 'w+')
    f.write("Number of users collected: %d\n" % (len(set(screenname_list))))
    f.write("Number of messages collected: %d\n" % (len(tweet_text)))
    f.write("Number of communities discovered: %d\n" % (len(clus_len)))
    f.write("Average number of users per community: %d\n" % (sum(clus_len) / len(clus_len)))
    f.write("Number of instances per class found:\n\t\t    Positive Class :%d\n\t\t    Negative Class :%d\n" % (clf[0], clf[1]))
    f.write("\nOne example from each class:\n\tExample from Positive Class:\n")
    
    for c1 in clf[2]:
        f.write("\tTweet: %s\n" % c1[0])
        f.write("\tpositive value: %d\n" % c1[1])
        f.write("\tnegative value: %d\n" % c1[2])

    f.write("\n\tExample from Negative Class:\n")
    
    
    for c2 in clf[3]:
        f.write("\tTweet: %s\n" % c2[0])
        f.write("\tpositive value: %d\n" % c2[1])
        f.write("\tnegative value: %d\n" % c2[2])
        

if __name__ == '__main__':
    main()