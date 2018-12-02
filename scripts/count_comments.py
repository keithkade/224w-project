# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 12:39:57 2018

@author: dimit_000
"""

# note: this file has 2,885,440 comments
comments_file = '/Volumes/TIME/reddit data/RC_filtered.txt'

comment_count = 0

print 'about to read the file'
for line in open(comments_file, 'r'):
    comment_count += 1
    if comment_count % 100000 == 0:
        print comment_count

print 'Total comments'
print comment_count
