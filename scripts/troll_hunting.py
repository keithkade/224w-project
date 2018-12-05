# -*- coding: utf-8 -*-
"""
Created on Wed Nov 07 20:07:49 2018

@author: dimit_000
"""

import pandas as pd
import datetime
import textstat
import re
from sklearn.mixture import GMM
import matplotlib.pyplot as plt
import numpy as np
from profanity import profanity

# comments_df = pd.read_csv('data/sample_comments.csv', sep='\t', encoding = 'utf-8')
# comments_df = pd.read_csv('data/2017_comments_1m_political.csv', sep='\t', encoding = 'utf-8')
comments_df = pd.read_csv('data/2017_comments_whitelist_capped.csv', sep='\t', encoding = 'utf-8')
comments_df = pd.read_csv('data/2017_comments_1m_political.csv', sep='\t', encoding = 'utf-8')

# Get the datetime of the comment
comments_df['comment_date_time'] = comments_df['retrieved_on'].apply(lambda x: str(datetime.datetime.fromtimestamp(x)))

comments_df.body.fillna('', inplace = True)

#### Post feature set ####
# Get the ARI of a post
comments_df['readability_index'] = comments_df['body'].apply(lambda x: textstat.automated_readability_index(x))
comments_df['readability_score'] = comments_df['body'].apply(lambda x: textstat.dale_chall_readability_score(x))
comments_df['reading_ease'] = comments_df['body'].apply(lambda x: textstat.flesch_reading_ease(x))
comments_df.loc[comments_df['reading_ease'] <0, 'reading_ease'] = 0
comments_df['reading_ease'] = comments_df['reading_ease'].max() - comments_df['reading_ease']
comments_df['difficult_words'] = comments_df['body'].apply(lambda x: textstat.difficult_words(x))
comments_df['post_standard'] = comments_df['body'].apply(lambda x: textstat.text_standard(x, True))
comments_df['profanity'] = comments_df['body'].apply(lambda x: profanity.contains_profanity(x))



 

# Splits the text into sentences, using  
# Spacy's sentence segmentation which can  
# be found at https://spacy.io/usage/spacy-101 
def break_sentences(text): 
    words = text.split()
    word_count = len(words)
    return word_count
    
# Get the number of words in a comment
comments_df['no_words'] = comments_df['body'].apply(lambda x: break_sentences(x))


#### Community feature set ####
# authors_df = pd.read_csv("data/sample_authors.csv")
authors_df = pd.read_csv('data/2017_authors.csv', encoding = 'utf-8')


#### Combine community and post feature sets and aggregate by author ####
authors_features = pd.merge(authors_df, comments_df, left_on = 'name', right_on = 'author')

# summarize features by user
authors_features = authors_features.groupby("name")[["comment_karma", "link_karma", "readability_index", "readability_score", "reading_ease", "difficult_words", "post_standard", "no_words", "score", "controversiality", "profanity"]].mean()

#### Cluster user features ####
X = authors_features.values
n_components = np.arange(1, 21)
models = [GMM(n, covariance_type='full', random_state=0).fit(X)
          for n in n_components]

# Estimate the number of clusters
plt.plot(n_components, [m.bic(X) for m in models], label='BIC')
plt.plot(n_components, [m.aic(X) for m in models], label='AIC')
plt.legend(loc='best')
plt.xlabel('n_components');

# Fit GMM
gmm = GMM(n_components=9).fit(X)
labels = gmm.predict(X)

# Append and interpret clusters
labels_df = pd.DataFrame(data=labels,    # values
              index=authors_features.index,    # 1st column as index
              columns=["label"])  

authors_features = authors_features.join(labels_df)

authors_features.groupby("label")[["comment_karma", "link_karma", "readability_index", "readability_score", "reading_ease", "difficult_words", "post_standard", "no_words", "score", "controversiality", "profanity"]].mean()

authors_features.label.value_counts()

authors_features[authors_features.index == "Diclicious666"]
authors_features[authors_features.index == "TheMadKing1988"]
authors_features[authors_features.index == "great_gape"]

cluster0_indices = np.where(labels==0)
authors_df.iloc[cluster0_indices]




# Check if we can do sentiment analysis
import nltk
from nltk.corpus import sentiwordnet as swn

text = comments_df.iloc[100, :]["body"]
token = nltk.word_tokenize(text)
tagged = nltk.pos_tag(token)
word_sentiment = swn.senti_synset('black.a.01')
word_sentiment.pos_score()
