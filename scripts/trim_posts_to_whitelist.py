import os
import pandas as pd
import json
import re

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

posts_files = ['/Volumes/TIME/reddit data/RS_2016-02', '/Volumes/TIME/reddit data/RS_2016-03']
out_file = '/Volumes/TIME/reddit data/RS_2016_filtered.txt'

invalid_names = set(['[deleted]'])

post_json_attributes_to_save = ['author', 'subreddit', 'subreddit_id',
'selftext', 'score', 'score', 'num_comments', 'id', 'title', 'ups', 'downs']

skip_count = 0
post_count = 0
with open(out_file, 'a') as f:
    for posts_file in posts_files:
        for line in open(posts_file, 'r'):
            post = json.loads(line)

            # sanitize the comment body
            post['selftext'] = re.sub('[^A-Za-z0-9]+', ' ', post['selftext'])
            post['title'] = re.sub('[^A-Za-z0-9]+', ' ', post['title'])

            if skip_count % 1000 == 0:
                print 'skipped:' + str(skip_count)

            if 'subreddit' not in post or post['subreddit'] not in whitelist: # skip non political subreddits
                skip_count += 1
                continue

            if post['author'] in invalid_names: # skip problem comments
                skip_count += 1
                continue

            post_count += 1

            # for testing
            if post_count % 1000 == 0:
                break

            if post_count % 10 == 0:
                print 'added:' + str(post_count)

            # don't save unnecessary stuff
            new_post = {}
            for attrib in post_json_attributes_to_save:
                new_post[attrib] = post[attrib]

            # write the comment to a new file
            f.write(json.dumps(new_post) + os.linesep)
