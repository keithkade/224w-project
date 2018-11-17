"""

To view in gephi, run this script, then load the csv as an edge list.
You'll also need to open the "Data Table" window and copy the data from the "id"
column into the "label" column and toggle "show labels" in the bottom left corner
of the view

"""

import csv
import os

from subreddits import get_filtered_subreddits
from settings import subreddit_subscriber_cutoff

node_id_to_info = {}

subreddits = get_filtered_subreddits(subreddit_subscriber_cutoff)

subreddit_count = len(subreddits)

for subreddit in subreddits:
    node_id_to_info[str(subreddit.Index)] = { 'type': 'subreddit', 'id': subreddit.base36_id, 'name': subreddit.name }

out_file = 'graphs/bipartite_connected_by_comment_folded_edgelist.csv'

if os.path.isfile(out_file):
    os.remove(out_file)

f = open(out_file, "a")
f.write('Source Target\n')

with open('graphs/bipartite_connected_by_comment_folded_edgelist.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')

    for row in csv_reader:
        if '#' not in row[0]:
            f.write(node_id_to_info[row[0]]['name'] + ' ' + node_id_to_info[row[1]]['name'] + '\n')
