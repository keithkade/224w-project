# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 12:39:57 2018
@author: dimit_000
"""

import pandas as pd
import json

posts_file = '/Volumes/TIME/reddit data/RS_2016_filtered.txt'

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

posts = []
post_count = 0
skip_count = 1
subreddit_post_counts = {}
for sub in whitelist:
    subreddit_post_counts[sub] = 0

print 'about to read the file'
for line in open(posts_file, 'r'):
    post = json.loads(line)

    if skip_count % 100000 == 0:
        print 'skipped:' + str(skip_count)

    if subreddit_post_counts[post['subreddit']] > 1000:
        skip_count += 1
        continue

    subreddit_post_counts[post['subreddit']] += 1

    post_count += 1
    if post_count % 1000 == 0:
        print 'added:' + str(post_count)

    posts.append(post)

print 'pruned ' + str(skip_count) + ' comments'
print 'used ' + str(post_count) + ' comments'

print subreddit_post_counts

print 'making dataframe'
posts_df = pd.DataFrame.from_dict(posts, orient='columns')

print 'Saving comments to csv'
posts_df.to_csv('data/2016_posts_whitelist_capped.csv', sep='\t', encoding = 'utf-8')

########################################## Create a users data frame from the comments
print 'Calculating authors'
authors_set = set()
for row in posts_df.itertuples():
    authors_set.add(row.author)

# make a list
users_jsons = []
for author in authors_set:
    users_jsons.append({'name': author})

# then a dataframe
users_df = pd.DataFrame(users_jsons)
users_df.to_csv('data/2016_post_authors.csv', encoding = 'utf-8')
