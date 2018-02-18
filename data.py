from twitter import *

import requests

nyt = requests.get("http://api.nytimes.com/svc/search/v2/articlesearch.json?q=propublica&begin_date=20161001&api-key=2205589d813c42acb5d34c5b729ce392")

t = Twitter(
    auth=OAuth('54091737-Te65diCAQ7QaQHI8lV86YQ8pqbvm3cK8zM4Scc5IR', 'Ytf6abfsuAj9kYqzYm6eA8JLz1okaygGXOpJGNjyopUCE', 'cHTThoqYt610bCrXxR1gVv6qr', 'NLmX22gq1pEuFW1J2RlFyErc55pEJ2TpMU3nY47Leec0NVLnhf'))

articles = nyt.json()

civic_tech = t.search.tweets(q="#civictech")