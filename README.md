# WeiboXCommunityNotes

## Code
### CommunityNotes.ipynb
A python notebook to collect #微博附注 data till Nov 2023. You need selenium (chrome driver: https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json).
You need to manually log in your weibo account after the browser opens the first page. The whole collection takes roughly a few hours. We should collect the latest keyword-hit posts every month.

### WeiboPosts.ipynb
A Python notebook to collect all noted Weibos from CommunityNotes.csv. It contains posts with endorsed notes, without any notes, or that are inaccessible now. 
No need to log in and this code takes longer time than CommunityNotes.ipynb. We should re-collect the latest posts every month and also try inaccessible posts again.


## Data
### CommunityNotes.csv
微博附注 data. The column names are easy to interpret. 

### TargetWeibos.csv
微博附注ed weibo posts. The column names are easy to interpret. Posts with endorsed notes have all variable values (even with multiple notes); posts without endorsed notes have no values in some variables; posts that are inaccessible by the time of data collections have only post link. It requires both post_link and user_name to match with CommunityNotes.csv

### Twitter Birdwatch/X Community Notes: https://twitter.com/i/communitynotes/download-data
