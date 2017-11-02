Collecting Political Social Network Data

In this Project, I've taken list of Twitter accounts of 4 U.S. presedential candidates from the previous election (2016). The list of 4 Candidates is in candidates.txt

The goal is to use the Twitter API to construct a social network of these accounts.
Then use the [networkx](http://networkx.github.io/) library to plot these links, as well as print some statistics of the resulting graph.

Steps:
1. Create an account on [twitter.com](http://twitter.com).
2. Generate authentication tokens by following the instructions [here](https://dev.twitter.com/docs/auth/tokens-devtwittercom).
3. Add your tokens to the key/token variables below. (API Key == Consumer Key)
4. Be sure you've installed the Python modules [networkx](http://networkx.github.io/) and [TwitterAPI](https://github.com/geduldig/TwitterAPI).

Assuming you've already installed [pip](http://pip.readthedocs.org/en/latest/installing.html), you can do this with `pip install networkx TwitterAPI`.

OK, now you're ready to start collecting some data!
