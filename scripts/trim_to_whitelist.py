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

# note: this file has 79,810,360 comments
comments_files = ['/Volumes/TIME/reddit data/RC_2017-05.txt', '/Volumes/TIME/reddit data/RC_2017-06.txt']

out_file = '/Volumes/TIME/reddit data/RC_filtered.txt'

invalid_names = set(['[deleted]', 'ithinkisaidtoomuch', 'Concise_AMA_Bot', 'AutoModerator'])

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
subreddit_comment_counts = {}
for sub in whitelist:
    subreddit_comment_counts[sub] = 0

os.remove(out_file)
with open(out_file, 'a') as f:
    for comments_file in comments_files:
        for line in open(comments_file, 'r'):
            comment = json.loads(line)

            # sanitize the comment body
            comment['body'] = re.sub('[^A-Za-z0-9]+', ' ', comment['body'])

            if skip_count % 100000 == 0:
                print 'skipped:' + str(skip_count)

            if comment['subreddit'] not in whitelist: # skip non political subreddits
                skip_count += 1
                continue

            if comment['author'] in invalid_names: # skip problem comments
                skip_count += 1
                continue

            comment_count += 1
            if comment_count % 100000 == 0:
                print 'added:' + str(comment_count)

            # don't save unnecessary stuff
            new_comment = {}
            for attrib in comment_json_attributes_to_save:
                new_comment[attrib] = comment[attrib]

            # write the comment to a new file
            f.write(json.dumps(new_comment) + os.linesep)
