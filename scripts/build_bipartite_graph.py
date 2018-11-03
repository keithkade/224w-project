import csv

subreddits_file = 'data/subreddits_basic.csv'
comments_file = 'data/sample_comments.json' # TODO do this from csv eventually

class SubReddit:
    def __init__(self, attr_array):
        self.base10_id        = attr_array[0]
        self.base36_id        = attr_array[1]
        self.creation_epoch   = attr_array[2]
        self.name             = attr_array[3]
        self.subscriber_count = attr_array[4]

    def __str__(self):
        return 'Subreddit name: ' + self.name + ', id: ' + self.base10_id

with open(subreddits_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        subreddit = SubReddit(row)
        print subreddit
