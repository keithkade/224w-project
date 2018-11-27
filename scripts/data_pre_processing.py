# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 12:39:57 2018

@author: dimit_000
"""

import os
import pandas as pd
import json
import re
from pprint import pprint
from settings import subreddit_subscriber_cutoff
from subreddits import get_filtered_subreddits

subreddits = get_filtered_subreddits(subreddit_subscriber_cutoff)

comment_json_attributes_to_save = ['author', 'body', 'controversiality',
'gilded', 'id', 'score', 'subreddit', 'subreddit_id']

# note: this file has at least 54,304,078 comments
comments_file = '/Volumes/TIME/reddit data/RC_2017-05.txt'

invalid_names = set(['[deleted]', 'ithinkisaidtoomuch', 'Concise_AMA_Bot', 'AutoModerator'])
valid_subs = set(map(lambda x: x.name, subreddits))
# mostly the defaults. also some with weirdly high comment count, and non-political ones
blacklist = set(['AskReddit', 'funny', 'pics', 'gaming', 'videos', 'movies',
'mildlyinteresting', 'OldSchoolCool', 'todayilearned', 'AdviceAnimals', 'gifs',
'aww', 'blog', 'books', 'food', 'askscience', 'Showerthoughts', 'photoshopbattles',
'photoshopbattles', 'gonewild', 'forhonor', 'RocketLeagueExchange', 'RocketLeague',
'Sneakers', 'GamingCircleJerk', 'counting', 'darksouls3', 'Warhammer40k',
'EliteDangerous', 'DnD', 'hearthstone', 'Drugs', 'Bitcoin', 'Anime', 'Ice_Poseidon'])

# white list generate with the following JS
# JSON.stringify(Array.from(document.getElementsByClassName('wiki')[0].getElementsByTagName('a')).map(x => x.href).filter(href => href.includes('/r/')).map(href => href.substring(href.indexOf('/r/')+3, href.length)).filter(href => !(href.includes('/') || href.includes('+'))))
# on https://www.reddit.com/r/politics/wiki/relatedsubs
whitelist = set(["BenCarson","ChrisChristie","TedCruz","Carly_Fiorina","Jindal",
"KasichForPresident","RandPaul","Marco_Rubio","RickSantorum","AskTrumpSupporters",
"The_Donald","HillaryClinton","HillaryForAmerica","MartinOMalley","SandersForPresident",
"GaryJohnson","JillStein","mcmullin","NeutralPolitics","centrist","moderatepolitics",
"peoplesparty","alltheleft","Classical_Liberals","democrats","demsocialist","greenparty",
"Labor","LeftCommunism","leninism","liberal","neoprogs","obama","progressive",
"SocialDemocracy","socialism","Conservative","Conservatives","Monarchism",
"new_right","objectivism","paleoconservative","republican","republicans",
"romney","TrueObjectivism","Agorism","anarcho_capitalism","anarchobjectivism",
"Christian_Ancaps","libertarian","LibertarianDebates","libertarianleft",
"libertarianmeme","LibertarianSocialism","LibertarianWomen","Paul","ronpaul",
"TrueLibertarian","voluntarism","communism","debateacommunist","DebateCommunism",
"Leftcommunism","Anarchism","anarchistnews","Anarchy101","CrimethincCollective",
"Green_Anarchism","LibertarianSocialism","LibertarianLeft","FuturistParty",
"PirateParty","BullMooseParty","ACTA","AntiWar","Bad_Cop_No_Donut","BadGovNoFreedom",
"CISPA","Democracy","EndlessWar","EnoughPaulSpam","EnoughObamaSpam","Environment",
"FairTax","FlushTheTPP","evolutionReddit","FirstAmendment","good_cop_free_donut",
"greed","Green","GunPolitics","gunsarecool","HumanRights","Labor","Liberty","NSA",
"NSALeaks","rpac","PoliticalActivism","privacy","ProChoice","ProGun","restorethefourth",
"rootstrikers","SaveTheConstitution","SocialDemocracy","SOPA","SupportTheTPP",
"Wikileaks","2012Elections","2016_elections","AmericansElect","Campaigns",
"ElectionPolls","ElectionReform","Elections","Forecast2016","PeoplesParty",
"RunForIt","Voting","MissouriPolitics","UtahPolitics","VirginiaPolitics",
"AmericanGovernment","AmericanPolitics","AnythingGoesNews","Ask_Political_Science",
"Ask_Politics","Authoritarian","comparative","Conspiracy","Conspiratard",
"DescentIntoTyranny","debatefascism","DoctorsWithoutBorders","Government","History",
"HumanRights","IWantOut","IWW","Justice","News","POLITIC","PoliticalDiscussion",
"PoliticalFactChecking","PoliticalHumor","PoliticalModeration","PoliticalPhilosophy",
"politicalpics","politicalpredictions","PoliticalScience","PoliticalTweets",
"PoliticsDebate","PoliticsInAmerica","pragmatism","RepublicOfPolitics","RvBdebates",
"StateoftheUnion","TechPolitics","ThirdPartyRoundTable","TruePolitics","USANews",
"USPolitics","WatchingCongress","wealth","WorldUnity","yro","AllOccupy","ACTA",
"Anonymous","AnonOps","AUInternetAccess","bad_cop_no_donut","BoycottHollywood",
"Cascadia","censorship","DarkNetPlan","evolutionReddit","FIA","HackBloc",
"InternetDeclaration","InternetDefense","IsraelExposed","KillHollywood","MeshNet",
"MensRights","Occupy","OccupyWallStreet","OpElectronicLeviathan","OperationGrabAss",
"OperationPullRyan","Petition","ProjectFactCheck","ProjectOverhaul","RedditActivism",
"RPAC","RWB","smallrevolutions","SOPA","TestPac","TimeToLegalize","TroubledTeens",
"CanadaPolitics","GeoPolitics","InternationalBusiness","InternationalPolitics",
"IRStudies","StrictlyWorldPolitics","SocialCitizens","UKPolitics","WorldEvents",
"Worldnews","WorldPoliticalHumour","Worldpolitics","Austrian_Economics","Business",
"Economics","InternationalBusiness"])

comments = []
comment_count = 0
skip_count = 0

print 'about to read the file'
for line in open(comments_file, 'r'):
    comment = json.loads(line)

    # sanitize the comment body
    comment['body'] = re.sub('[^A-Za-z0-9]+', ' ', comment['body'])

    if comment['author'] in invalid_names: # skip problem comments
        skip_count += 1
        continue

    if comment['subreddit'] not in valid_subs: # skip long tail of niche subreddits
        # print comment['subreddit']
        skip_count += 1
        continue

    # if comment['subreddit'] in blacklist: # skip popular non political subreddits
    #     skip_count += 1
    #     continue

    if comment['subreddit'] not in whitelist: # skip non political subreddits
        skip_count += 1
        continue

    comment_count += 1
    if comment_count % 1000 == 0:
        print comment_count

    if comment_count > 1000000:
        break

    # don't save unnecessary stuff
    new_comment = {}
    for attrib in comment_json_attributes_to_save:
        new_comment[attrib] = comment[attrib]

    comments.append(new_comment)

print 'pruned ' + str(skip_count) + ' comments'

print 'making dataframe'
comments_df = pd.DataFrame.from_dict(comments, orient='columns')

print 'Saving comments to csv'
comments_df.to_csv('data/2017_comments_1m_political.csv', sep='\t', encoding = 'utf-8')

########################################## Create a users data frame from the comments
print 'Calculating authors'
authors_set = set()
for row in comments_df.itertuples():
    authors_set.add(row.author)

# make a list
users_jsons = []
for author in authors_set:
    users_jsons.append({'name': author})

# then a dataframe
users_df = pd.DataFrame(users_jsons)

print 'Saving comments to csv'

users_df.to_csv('data/2017_users_1m_political.csv', encoding = 'utf-8')

# Authors: includes users' karma used for troll detection
authors = []
for line in open('data\2016_authors.json', 'r'):
    author = json.loads(line)
    if author['name'] in users_df.name.values:
        authors.append(author)

authors_df = pd.DataFrame([])
for author in authors:
    df = pd.DataFrame.from_dict([comment], orient='columns')
    authors_df = comments_df.append(df)

authors_df.to_csv('data/2017_authors.csv', encoding = 'utf-8')
