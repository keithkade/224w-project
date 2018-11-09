from subreddits import get_filtered_subreddits
from users import users
from comments import comments

subs = get_filtered_subreddits(10000)


user_comment_counts = {}
for user in users:
    user_comment_counts[user.name] = 0

for comment in comments:
    user_comment_counts[comment.author] += 1

for comment in comments:
    if comment.author in user_comment_counts and user_comment_counts[comment.author] > 100:
        del user_comment_counts[comment.author]

sub_comment_counts = {}

for comment in comments:
    if comment.subreddit_id in sub_comment_counts:
        sub_comment_counts[comment.subreddit_id] += 1
    else:
        sub_comment_counts[comment.subreddit_id] = 1

print len(list(sub_comment_counts.keys()))


print sum(list(sub_comment_counts.values()))/float(len(list(sub_comment_counts.keys())))

# print sum(list(user_comment_counts.values()))/float(len(list(user_comment_counts.keys())))
