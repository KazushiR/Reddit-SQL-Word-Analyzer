import praw, os, json, time, nltk, sqlite3
from praw.models import MoreComments #Reddit API
from collections import Counter
from nltk.tag import pos_tag #Word counter
from nltk.tokenize import word_tokenize

times = 15

Nouns = {}
Universal_Nouns =  {}
all_nouns = Counter()

os.chdir(r"C:\Users\Kazushi Rickert\Desktop\PythonProjects\Python\Python projects\Python Praw\Python_Praw_Bot")
with open("config_cred.json") as r: #Opens the credentials the access the reddit API
    data = json.load(r)
    reddit = praw.Reddit(client_id = data["client_id"],
                     client_secret = data["client_secret"],
                     username = data["username"],
                     password = data["password"],
                     user_agent = data["user_agent"])
    r.close()

subred = reddit.subreddit("aww")# Gets information/oomments from a particular subreddit

#print(dir(x))

count = 0
for i in subred.hot(limit = times):
    subreddit_id=i.id
    print(i.title)
    submission = reddit.submission(id=subreddit_id)
    
    submission.comment_limit = times
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        new_comments = top_level_comment.body.split()
        tokenized = pos_tag(nltk.word_tokenize(top_level_comment.body))
        Universal_tokenized = pos_tag(nltk.word_tokenize(top_level_comment.body), tagset = "universal")
        _ = {i for i in tokenized if i[1] == "NN"}
        __ = {i[0].lower():i[1].lower() for i in Universal_tokenized if i[1] == "NOUN"}
        Nouns.update(_)
        Universal_Nouns.update(__)
for i in Nouns:
    all_nouns[i.lower()] += 1
Final_Nouns = {i:j  for i, j in all_nouns.items() if i.lower() in Universal_Nouns}
new_final_nouns = sorted(Final_Nouns.items(), key = lambda x:x[1], reverse = True)





