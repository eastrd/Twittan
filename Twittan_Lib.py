import requests as rq
import time as t
import Twittan_Const as const
from bs4 import BeautifulSoup as bs

#Username List waiting to be scraped
usernamePool = []
scrapedUsernamePool = []
TweetCount = 0



def checkIfLimitedAttempt(url):
	#Check for Blocking Attempts and sleep if YES
	while True:
		soup = bs(rq.get(url).content,"html.parser")
		found = soup.find("div",class_="subtitle")
		if found is None:
			return soup
		print "Detected limiting Attempt, sleeping for 4 secs..."
		t.sleep(4)


def ScrapeIndexPageUsers():
	IndexPageSoup = checkIfLimitedAttempt(const.URL_MainSite)
	return getUsernames(IndexPageSoup)


def getName(soup):
	return soup.find("div",class_="fullname").text.replace("\n","").replace("  ","")


def getLocation(soup):
	return soup.find("div",class_="location").text.replace("\n","").replace(" ","")


def getPersonalInfo(soup):
	name = getName(soup)
	location = getLocation(soup)
	return "Username: "+username+"\nName: "+name+"\nLocation: "+location


def ScrapeUserProfileWall(username):
	PersonURL = const.URL_MainSite+username
	WallSoup = checkIfLimitedAttempt(PersonURL)
	print getPersonalInfo(WallSoup)
	while True:
		scrapeTweets(WallSoup)
		NextPageURL = getNextPageURL(WallSoup)
		if NextPageURL is None:
			print "Scraped Tweets: "+str(TweetCount)
			break
		WallSoup = checkIfLimitedAttempt(NextPageURL)
	usernamePool.extend(getFollowingUsers(username))
	usernamePool.extend(getFollowerUsers(username))
	print "\n"


def scrapeTweets(soup):
	global TweetCount
	if checkIfAccIsPrivate(soup) == False:
		for tweets in soup.find_all("table",{"class":"tweet"}):
			Date = tweets.find("td",class_="timestamp").text.encode("utf-8").replace("\n","")
			Context = tweets.find("div",class_="tweet-text").text.encode("utf-8").replace("\n","")			
			print "-"+Date+"->"+Context
			TweetCount = TweetCount+1
	else:
		print const.BANNER_AccIsPrivate


def getNextPageURL(Soup):
	info = Soup.find("div",class_="w-button-more")
	return const.URL_MainSite+info.find("a")["href"] if (info is not None) else None
		

def getFollowingURL(username):
	return const.URL_MainSite+username+"/following"


def getFollowersURL(username):
	return const.URL_MainSite+username+"/followers"


def getUsernames(soup,unwantedUsername = ""):
	userList = []
	for usernameRAW in soup.find_all("span", {"class":"username"}):
		cleanUsername = usernameRAW.text.replace("@","")
		if cleanUsername != unwantedUsername:
			userList.append(cleanUsername)
	return userList

def checkIfEmptyFollow(soup):
	return True if (soup.find("span",class_="username") == None) else False

def checkIfAccIsPrivate(soup):
	return False if (soup.find("div",class_="protected") == None) else True


def getFollowerUsers(username):
	#Loop and get all Followers
	RelatedUserList = []
	URL = getFollowersURL(username)
	while True:
		FollowerSoup = checkIfLimitedAttempt(URL)
		if checkIfEmptyFollow(FollowerSoup) == True:
			return
		Users = getUsernames(FollowerSoup,username)
		RelatedUserList.extend(Users)
		NextPageURL = getNextPageURL(FollowerSoup)
		if NextPageURL == None:
			print str(len(RelatedUserList))+" Followers"
			return RelatedUserList
		URL = NextPageURL
		

def getFollowingUsers(username):
	#Loop and get all Followings
	RelatedUserList = []
	URL = getFollowingURL(username)		#Starting URL to scrape
	while True:
		FollowingSoup = checkIfLimitedAttempt(URL)
		if checkIfEmptyFollow(FollowingSoup) == True:
			return
		Users = getUsernames(FollowingSoup,username)
		RelatedUserList.extend(Users)
		NextPageURL = getNextPageURL(FollowingSoup)
		if NextPageURL == None:
			print str(len(RelatedUserList))+" Followings"
			return RelatedUserList
		URL = NextPageURL


#	Main Function	#
usernamePool.extend(ScrapeIndexPageUsers())
for username in usernamePool:
	if username not in scrapedUsernamePool:
		ScrapeUserProfileWall(username)
		scrapedUsernamePool.append(username)
	usernamePool.remove(username)