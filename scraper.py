import praw
import sys
import os
import django
from time import sleep, time


os.environ.setdefault("DJANGO_SETTINGS_MODULE","TheOnionGame.settings")
django.setup()

from game.models import Article

#Application only OAuth
r = praw.Reddit(
    client_id='tRCD8jbGwZkRjA',
    client_secret='4U6cDA7Y4cfFgK3m4EZB0IxVmXw',
    user_agent='Scraping bot with the purpose of gathering submissions from r/NotTheOnion and r/TheOnion'
)

def filterName(t):
    while t.find(":") != -1:
        #strip the headline/introductory-esque phrase from the start of the title
        index = t.find(":")
        t = t[index+2:]
    return t

REAL = True
FAKE = False
prev = REAL

articlesAdded = 0

maxAttempts = 10 #maximum attempts before it switches to next type (real/fake)
currentAttempts = 0

while True:
    try:
        sys.stdout.write("\r"+str(articlesAdded)+f" added to the database ({Article.objects.count()} total)")
        sys.stdout.flush()
        if prev == REAL:
            #current = FAKE
            subreddit = r.subreddit("theonion")
        else:
            #current = REAL
            subreddit = r.subreddit("nottheonion")

        submission = subreddit.random()
        while submission.is_self:
            #Fail-safe (probably useless)
            submission = subreddit.random()

        title = submission.title
        if prev == REAL: #currently The Onion (real)
            title = filterName(title)

        if Article.objects.filter(title=title).count() != 0:
            currentAttempts += 1
            if currentAttempts >= maximumAttempts:
                currentAttempts = 0
                prev = not prev
            continue

        Article.objects.create(
            title=title,
            url=submission.url,
            real=(not prev)
        )
        articlesAdded += 1
        prev = not prev
    except Exception as e:
        pass
