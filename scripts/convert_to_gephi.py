"""

To view in gephi, run this script, then load the csv as an edge list.
You'll also need to open the "Data Table" window and copy the data from the "id"
column into the "label" column and toggle "show labels" in the bottom left corner
of the view

"""

import csv
import os

from subreddits import subreddits
from settings import graph_str

node_id_to_info = {}

subreddit_count = len(subreddits)

for subreddit in subreddits:
    node_id_to_info[str(subreddit.Index)] = { 'type': 'subreddit', 'id': subreddit.base36_id, 'name': subreddit.name }

out_file = 'gephi/'+graph_str+'.csv'

if os.path.isfile(out_file):
    os.remove(out_file)

f = open(out_file, "a")
f.write('Source Target\n')

with open(graph_str+'.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')

    for row in csv_reader:
        if '#' not in row[0]:
            f.write(node_id_to_info[row[0]]['name'] + ' ' + node_id_to_info[row[1]]['name'] + '\n')
