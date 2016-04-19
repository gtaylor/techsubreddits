import time
from techsubs.sr_scanner import api_client

r = api_client.get_praw_client()
# sr = r.get_subreddit('python')
# print sr.subscribers
query = 'timestamp:%s..%s' % (
    int(time.time() - (3600 * 24)),
    int(time.time()))
results = r.search(query, subreddit='python', sort='new', limit=100, syntax='cloudsearch')
counter = 0
for result in results:
    print result
    counter += 1
print "Total posts", counter
