"""
How the flow works.

There are a number of steps to this process. The settings control things along the way.
The original comment, post, and author files are on google drive because they are really big.
They were generated with the 'trim_to_whitelist' scripts. Put them all in the same directory
and note that with the raw_data_location setting

To make a new graph

First run the cap_posts|comments scripts. That reads the raw comments and,
caps them according to any threshold, and generates comment, post, and author csvs. You
only need to run this step whenever you change the comments_cap, posts_cap, or year variables.
This takes a while (20-30 minutes), in particular the scanning of all the users and gathering their info.
There are over 66,100,000 users.

Then run build_bipartite_graph.py. It will generate edglist graph files in the format below:

---------------------------FILE FORMATS---------------------------

Graphs are generated with the following names
<year>-<N><posts|comments>-<N><CommentCap>-<N><PostCap>-<deconvolved>-<trolls>

<year>: the year of data. either 3 months from 2016 or 2 months from 2017

<N><posts|comments>: whether subreddits and user are connected by posts,
comments, or both, and how many (N) users in common are required for two subreddits to become
connected during folding

<N><CommentCapped>: the number of comments allowed per subreddit

<N><PostCapped>: the number of posts allowed per subreddit

<deconvolved>: whether the graph is deconvolved

<trolls>: whether it's just trolls, no trolls, or everyone

with both a .txt extension and a .csv extension. the .txt is for SNAP, the .csv is for Gephi

all graphs use only the whitelisted subreddits
"""

#consts
subreddits_csv = 'data/subreddits.csv'
bipartite_graph_file = 'graphs/bipartite_graph.graph'

# variables in data pre processing
raw_data_location = '/data/'
year = '2016'
comments_cap = 1000
posts_cap = 1000

# variables in graph folding
connect_via_post = True
post_connection_threshold = 1 # haven't tried changing this yet
connect_via_comment = False
comment_connection_threshold = 1 # haven't tried changing this yet

fold_connection_threshold = 5
should_deconvolve = False
just_trolls = False # if this is true, make remove trolls false
remove_trolls = True
show_networkx_deconvolved = False
compute_communities = True
compute_hits = False

"""
Some scores for certain graphs

GENERATED GRAPH: graphs/2016-3comments-1000CommentCap--_just-trolls
=============Metrics for rewired=============
Completeness: 0.369070246429
=============Metrics for generated=============
Completeness: 0.579380164286
Difference: 0.210309917857

GENERATED GRAPH: graphs/2016-5comments-1000CommentCap--_
=============Metrics for rewired=============
Completeness: 0.242966121584
=============Metrics for generated=============
Completeness: 0.521165499398
Difference: 0.278199377814

GENERATED GRAPH: graphs/2016-5comments-1000CommentCap--_without_trolls
=============Metrics for rewired=============
Completeness: 0.353493683379
=============Metrics for generated=============
Completeness: 0.652223699671
Difference: 0.298730016292

GENERATED GRAPH: graphs/2016-5comments-1000CommentCap--deconvolved_
=============Metrics for rewired=============
Completeness: 0.526215201148
=============Metrics for generated=============
Completeness: 0.643298377467
Difference: 0.117083176319

GENERATED GRAPH: graphs/2016-5comments-1000CommentCap--deconvolved_without_trolls
=============Metrics for rewired=============
Completeness: 0.531373301291
=============Metrics for generated=============
Completeness: 0.643993886322
Difference: 0.112620585031



GENERATED GRAPH: graphs/2016-1posts--1000PostCap-_just-trolls
=============Metrics for rewired=============
Completeness: 0.49022687927546366
=============Metrics for generated=============
Completeness: 0.6262057184876308
Difference: 0.1359788392121672

GENERATED GRAPH: graphs/2016-5posts--1000PostCap-_
=============Metrics for rewired=============
Completeness: 0.36869124459668073
=============Metrics for generated=============
Completeness: 0.5544329460997891
Difference: 0.18574170150310837

GENERATED GRAPH: graphs/2016-5posts--1000PostCap-_without_trolls
=============Metrics for rewired=============
Completeness: 0.30531334918739417
=============Metrics for generated=============
Completeness: 0.49868548481142017
Difference: 0.193372135624026

"""

comments_csv = 'data/'+year+'_comments_'+str(comments_cap)+'capped.csv'
posts_csv = 'data/'+year+'_posts_'+str(posts_cap)+'capped.csv'
comment_authors_csv = 'data/'+year+'_comment-authors_'+str(comments_cap)+'capped.csv'
post_authors_csv = 'data/'+year+'_post-authors_'+str(posts_cap)+'capped.csv'

posts_str = 'posts' if connect_via_post else ''
comments_str = 'comments' if connect_via_comment else ''
deconvolved_str = 'deconvolved' if should_deconvolve else ''
comments_cap_str = str(comments_cap)+'CommentCap' if connect_via_comment else ''
posts_cap_str = str(posts_cap)+'PostCap' if connect_via_post else ''

trolls_str = ''
if remove_trolls:
    trolls_str = 'without_trolls'
elif just_trolls:
    trolls_str = 'just-trolls'

graph_str = 'graphs/'+year+'-'+str(fold_connection_threshold)+posts_str+comments_str+'-'+comments_cap_str+'-'+posts_cap_str+'-'+deconvolved_str+'_'+trolls_str
trolls_csv = 'data/'+year+'_trolls.csv'
plot_str = 'plots/'+year+'-'+str(fold_connection_threshold)+posts_str+comments_str+'-'+comments_cap_str+'-'+posts_cap_str+'-'+deconvolved_str+'_'+trolls_str

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

# from the /r/politics related subreddit lists
categories_to_subreddit = {
    "republicans_candidates": set(["BenCarson","ChrisChristie","TedCruz","Carly_Fiorina","Jindal","KasichForPresident","RandPaul","Marco_Rubio","RickSantorum","AskTrumpSupporters","The_Donald"]),
    "democratic_candidates": set(["HillaryClinton","HillaryForAmerica","MartinOMalley","SandersForPresident"]),
    "third_party_candidates": set(["GaryJohnson","JillStein","mcmullin"]),
    "partisan_center": set(["NeutralPolitics","centrist","moderatepolitics","peoplesparty"]),
    "partisan_left": set(["alltheleft","Classical_Liberals","democrats","demsocialist","greenparty",
    "Labor","LeftCommunism","leninism","liberal","neoprogs","obama","progressive",
    "SocialDemocracy","socialism"]),
    "partisan_right": set(["Conservative","Conservatives","Monarchism","new_right","objectivism","paleoconservative","republican","republicans","romney","TrueObjectivism"]),
    "libertarian": set(["Agorism","anarcho_capitalism","anarchobjectivism","Christian_Ancaps","libertarian","LibertarianDebates","libertarianleft","libertarianmeme","LibertarianSocialism","LibertarianWomen","Paul","ronpaul","TrueLibertarian","voluntarism"]),
    "communism": set(["communism","debateacommunist","DebateCommunism","Leftcommunism"]),
    "anarchism": set(["Anarchism","anarchistnews","Anarchy101","CrimethincCollective","Green_Anarchism","LibertarianSocialism","LibertarianLeft"]),
    "other_parties": set(["FuturistParty","PirateParty","BullMooseParty"]),
    "issues": set(["ACTA","AntiWar","Bad_Cop_No_Donut","BadGovNoFreedom","CISPA","Democracy","EndlessWar","EnoughPaulSpam","EnoughObamaSpam","Environment","FairTax","FlushTheTPP","evolutionReddit","FirstAmendment","good_cop_free_donut","greed","Green","GunPolitics","gunsarecool","HumanRights","Labor","Liberty","NSA","NSALeaks","rpac","PoliticalActivism","privacy","ProChoice","ProGun","restorethefourth","rootstrikers","SaveTheConstitution","SocialDemocracy","SOPA","SupportTheTPP","Wikileaks"]),
    "election": set(["2012Elections","2016_elections","AmericansElect","Campaigns","ElectionPolls","ElectionReform","Elections","Forecast2016","PeoplesParty","RunForIt","Voting"]),
    "state_specific": set(["MissouriPolitics","UtahPolitics","VirginiaPolitics"]),
    "general_interest": set(["AmericanGovernment","AmericanPolitics","AnythingGoesNews","Ask_Political_Science","Ask_Politics","Authoritarian","comparative","Conspiracy","Conspiratard","DescentIntoTyranny","debatefascism","DoctorsWithoutBorders","Government","History","HumanRights","IWantOut","IWW","Justice","News","POLITIC","PoliticalDiscussion","PoliticalFactChecking","PoliticalHumor","PoliticalModeration","PoliticalPhilosophy","politicalpics","politicalpredictions","PoliticalScience","PoliticalTweets","PoliticsDebate","PoliticsInAmerica","pragmatism","RepublicOfPolitics","RvBdebates","StateoftheUnion","TechPolitics","ThirdPartyRoundTable","TruePolitics","USANews","USPolitics","WatchingCongress","wealth","WorldUnity","yro"]),
    "activist_network": set(["AllOccupy","ACTA","Anonymous","AnonOps","AUInternetAccess","bad_cop_no_donut","BoycottHollywood","Cascadia","censorship","DarkNetPlan","evolutionReddit","FIA","HackBloc","InternetDeclaration","InternetDefense","IsraelExposed","KillHollywood","MeshNet","MensRights","Occupy","OccupyWallStreet","OpElectronicLeviathan","OperationGrabAss","OperationPullRyan","Petition","ProjectFactCheck","ProjectOverhaul","RedditActivism","RPAC","RWB","smallrevolutions","SOPA","TestPac","TimeToLegalize","TroubledTeens"]),
    "international_politics": set(["CanadaPolitics","GeoPolitics","InternationalBusiness","InternationalPolitics","IRStudies","StrictlyWorldPolitics","SocialCitizens","UKPolitics","WorldEvents","Worldnews","WorldPoliticalHumour","Worldpolitics"]),
    "economics": set(["Austrian_Economics","Business","Economics","InternationalBusiness"]),
}

subreddit_to_category = {}
i = 0
for cat in categories_to_subreddit:
    i += 1
    for sub in categories_to_subreddit[cat]:
        subreddit_to_category[sub] = i
