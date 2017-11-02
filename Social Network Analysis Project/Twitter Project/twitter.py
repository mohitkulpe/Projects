# coding: utf-8

# Imports you'll need.
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI
from itertools import combinations


consumer_key = 'Provide Your Consumer Key'
consumer_secret = 'Provide Your Consumer Secret'
access_token = 'Provide Your Access Token'
access_token_secret = 'Provide Your Access Token Secret'



def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    
    
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def read_screen_names(filename):
    """
    Read a text file containing Twitter screen_names, one per line.

    Params:
        filename....Name of the file to read.
    Returns:
        A list of strings, one per screen_name, in the order they are listed
        in the file.

    
    ###TODO
    

    with open("C:/Users/Mohit/mohitkulpe/a0/candidates.txt", "rt") as in_file:
        MyList = [line.strip('\n') for line in in_file]
        
    return(MyList)
    
    pass


# I've provided the method below to handle Twitter's rate limiting.
# You should call this method whenever you need to access the Twitter API.

def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def get_users(twitter, screen_names):
    """Retrieve the Twitter user objects for each screen_name.
    Params:
        twitter........The TwitterAPI object.
        screen_names...A list of strings, one per screen_name
    Returns:
        A list of dicts, one per user, containing all the user information
        (e.g., screen_name, id, location, etc)

    See the API documentation here: https://dev.twitter.com/rest/reference/get/users/lookup

    """
    ###TODO
    
    
    request = robust_request(twitter,'users/lookup', {'screen_name': screen_names},max_tries=5)
    #print (type(request))
    return request
    
    
    pass


def get_friends(twitter, screen_name):
    """ Return a list of Twitter IDs for users that this person follows, up to 5000.
    See https://dev.twitter.com/rest/reference/get/friends/ids

    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.

    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
    Returns:
        A list of ints, one per friend ID, sorted in ascending order.

    Note: If a user follows more than 5000 accounts, we will limit ourselves to
    the first 5000 accounts returned.

    ###TODO
    
    request = robust_request(twitter,'friends/ids', {'screen_name': screen_name, 'count' : 5000},max_tries=5)
    list_res = [r for r in request]
    sorted_list = (sorted(list_res))
    return sorted_list
    
    pass


def add_all_friends(twitter, users):
    """ Get the list of accounts each user follows.
    I.e., call the get_friends method for all 4 candidates.

    Store the result in each user's dict using a new key called 'friends'.

    Args:
        twitter...The TwitterAPI object.
        users.....The list of user dicts.
    Returns:
        Nothing

    ###TODO
    for i in range (len(users)):
        friend_id = get_friends(twitter, users[i]['screen_name'])
        
        users[i]['friends']=friend_id
    pass


def print_num_friends(users):
    """Print the number of friends per candidate, sorted by candidate name.
    See Log.txt for an example.
    Args:
        users....The list of user dicts.
    Returns:
        Nothing
    """
    ###TODO
    #print (users[0])
    
    for i in range (len(users)):
         current_user = users[i]
         friend_list = current_user['friends']
         print (current_user['screen_name'], len(friend_list))
          
        
         #sort_num_friends = sorted(combine, key=lambda x: x[2], reverse=True)
    
    return
    
    pass


def count_friends(users):

    """ Count how often each friend is followed.
    Args:
        users: a list of user dicts
    Returns:
        a Counter object mapping each friend to the number of candidates who follow them.
        Counter documentation: https://docs.python.org/dev/library/collections.html#collections.Counter

    
    """
    ###TODO
    common_friends = []
    
    for i in range (len(users)):
        common_friends = common_friends + (users[i]['friends'])
        
    return Counter(common_friends)
   
    #print (common_friends)
    
    pass


def friend_overlap(users):
    """
    Compute the number of shared accounts followed by each pair of users.

    Args:
        users...The list of user dicts.

    Return: A list of tuples containing (user1, user2, N), where N is the
        number of accounts that both user1 and user2 follow.  This list should
        be sorted in descending order of N. Ties are broken first by user1's
        screen_name, then by user2's screen_name (sorted in ascending
        alphabetical order). See Python's builtin sorted method.

    
    """
    ###TODO
    overlapping_count = []
    frnd_comb = []
    
    candidate = []
    for i in users:
        candidate.append(i['screen_name'])
    #print ('\n',candidate)
    
    
    comb = combinations(candidate, 2)
    
    for j in comb:
         frnd_comb.append(j)
         
         can1_index = next(index for (index, d) in enumerate(users) if d["screen_name"] == j[0])
         can2_index = next(index for (index, d) in enumerate(users) if d["screen_name"] == j[1])
    #print (can1_index, can2_index)  
        
         can1_frnd = users[can1_index]['friends']
         can2_frnd = users[can2_index]['friends']
   # print (can1_frnd)
         frnd_overlap = set(can1_frnd).intersection(can2_frnd)
   # print len(frnd_overlap)
         overlapping_count.append(len(frnd_overlap))
      
    
   # print ('\n',frnd_comb)
    #print (overlapping_count)
    

    combine = []

    for i in range(0,len(overlapping_count)):
        combine1 = frnd_comb[i]
        combine1 = combine1 + (overlapping_count[i],)
        combine.append(combine1)
   
    #print ('\n',(combine))
            
    sort_combine = sorted(combine, key=lambda x: x[2], reverse=True)
    
    return sort_combine
          
    pass


def followed_by_hillary_and_donald(users, twitter):
    """
    Find and return the screen_name of the one Twitter user followed by both Hillary
    Clinton and Donald Trump. You will need to use the TwitterAPI to convert
    the Twitter ID to a screen_name. See:
    https://dev.twitter.com/rest/reference/get/users/lookup

    Params:
        users.....The list of user dicts
        twitter...The Twitter API object
    Returns:
        A string containing the single Twitter screen_name of the user
        that is followed by both Hillary Clinton and Donald Trump.
    """
    ###TODO
    
    hillary_index = next(index for (index, d) in enumerate(users) if d["screen_name"] == "HillaryClinton")
   # print (hillary_index)

    donald_index = next(index for (index, d) in enumerate(users) if d["screen_name"] == "realDonaldTrump")
   # print (donald_index)

    hillary_friend = users[hillary_index]['friends']
    donald_friend = users[donald_index]['friends']
    #print (hillary_friend)
    #print (donald_friend)

    common = []
    for element in hillary_friend:
        if element in donald_friend:
            common.append(element)
   
    #print ('\n',common)
        
       
    for i in range(0,len(common)):
        
        request = robust_request(twitter,'users/lookup', {'user_id': common[i]},max_tries=5)

        json_res = request.json()
    #print(json_res)
    
        name = json_res[i]['screen_name']
        
    return (str(name))
    pass


def create_graph(users, friend_counts):
    """ Create a networkx undirected Graph, adding each candidate and friend
        as a node.  Note: while all candidates should be added to the graph,
        only add friends to the graph if they are followed by more than one
        candidate. (This is to reduce clutter.)

        Each candidate in the Graph will be represented by their screen_name,
        while each friend will be represented by their user id.

    Args:
      users...........The list of user dicts.
      friend_counts...The Counter dict mapping each friend to the number of candidates that follow them.
    Returns:
      A networkx Graph
    """
    ###TODO
    G = nx.Graph()
    
    for user in users:
        G.add_node(user['screen_name'])
        for friend_id in user['friends']:
            if friend_id in friend_counts:
                if friend_counts[friend_id] > 1:
                    G.add_node(friend_id)
                    G.add_edge(user['screen_name'], friend_id)
                    
                    
    return G
        
    
    pass


def draw_network(graph, users, filename):
    """
    Draw the network to a file. Only label the candidate nodes; the friend
    nodes should have no labels (to reduce clutter).

    Methods you'll need include networkx.draw_networkx, plt.figure, and plt.savefig.

    Your figure does not have to look exactly the same as mine, but try to
    make it look presentable.
    """
    ###TODO
    
    graph_label = {}
    for i in users:
        graph_label [i['screen_name']] = i['screen_name']
    
    plt.figure(figsize=(15,12))
    nx.draw_networkx(graph,labels=graph_label,node_color='mediumorchid',width=.5,alpha=.7,font_color='red',font_weight='bold',font_size=15)
    
    plt.savefig(filename)
    
    pass


def main():
    """ Main method. You should not modify this. """
    twitter = get_twitter()
    screen_names = read_screen_names('candidates.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    #print (type(users))
    print('found %d users with screen_names %s' %
          (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    print('Friends per candidate:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    print('User followed by Hillary and Donald: %s' % followed_by_hillary_and_donald(users, twitter))

    graph = create_graph(users, friend_counts)
    print ('Network Graph: graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph, users, 'network.png')
    print('network drawn to network.png')


if __name__ == '__main__':
    main()

