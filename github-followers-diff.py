#!/usr/bin/python3
import re
import requests
import sys

def getLogins(base_url):
	headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	page = 1;
	i = 1
	followers = []
	while i<=page:
		url = base_url+'?page='+str(i)
		response = None;
		try:
			response = requests.get(url=url,headers=headers)
		except:
			print("something wrong")
		if i == 1:
			if 'Link' not in response.headers:
				print("Can't get logins")
				return followers 
			match = re.search(r'next.*?page=(\d+)', response.headers['Link'])
			if match:
				page = int(match.group(1))
		items = response.json() 
		for j in range(0,len(items)):
			followers.append(items[j]['login'])
		i+=1
	return followers

def getFollowers(user):	
	return getLogins('https://api.github.com/users/'+user+'/followers')

def getFollowing(user):	
	return getLogins('https://api.github.com/users/'+user+'/following')

def getDiff(user):
	followers = getFollowers(user)
	following = getFollowing(user)
	diff = []

	for follower in followers:
		isFollower = False
		for followi in following:
			if follower == followi:
				isFollower = True
				break
		if not isFollower:
			diff.append(follower)
	
	for followi in following:
		isFollowi = False
		for follower in followers:
			if follower == followi:
				isFollowi = True
				break
		if not isFollowi:
			diff.append(followi)
	
	return diff

if len(sys.argv)>1:
	items = getDiff(sys.argv[1])
	for item in items:
		print(item)
else:
	print("add a user")
	print(sys.argv[0] + " user")

