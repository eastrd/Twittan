									Twittan Log
23/03/2016:
	- Twittan Project Launched
	- Made some basic functions: scraping users, usernames from tweet wall and tweets
	- Made a detection function for twitter limiting attempts
24/03/2016:
	- Bug Fixed for not scraping all the tweets, b/c didn't detect the attempts limitation during scraping
	- Updated functions for scraping dates and tweets together, added functions for scraping all the follower and following usernames and loop through the expanding network
	- Updated to make the program to iterate through pages in order to scrape all the tweets
	- Found that Twitter has limited some users' tweets to approx 3000
	- Bug Found: Connection Aborted Error 10053, said to be client closing the sockets, have tried turning firewall off but no luck
	- N.B Code is redundant, need to refactor!!!
25/03/2016:
	- Optimised the limit checking function
	- Refactored some logics
	- Created a file to store constant strings
	- Modified some lines into more pythonic styles of coding
	- Renamed some functions
	- Splited some massive function chunks into smaller ones
	- Give up on Titan-DB and Mogwai due to limited support and complex setup environment, decided to move to Redis.
	