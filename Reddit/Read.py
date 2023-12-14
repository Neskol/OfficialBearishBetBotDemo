import json
import praw
from datetime import datetime
import os

def get_new_posts():
    reddit = praw.Reddit("BearishBetsBot")
    subreddit = reddit.subreddit('wallstreetbets')
    posts = []
    # Newest Post in r/wallstreetbets
    for post in subreddit.new(limit=1000):
        created_utc = datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        posts.append({
            'score': post.score,
            'title': post.title,
            'selftext': post.selftext,
            'score': post.score,
            'created_utc': created_utc,
        })

    # New File Name
    datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    rel_file_path = f"../Data/new_posts_{datetime_str}.json"
    # New File Path
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, rel_file_path)
    # Dump posts in a timestamped new file
    with open(abs_file_path, 'w') as f:
        json.dump(posts, f, indent=2)

# Run
get_new_posts()