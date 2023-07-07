import requests
from bs4 import BeautifulSoup
import csv

def getDetails(content):
	elements = content.find_all("span", class_="go-Main-headerDetailItem")
	## cycle through all the details and pull out relevant items
	details = []	
	for element in elements:
		text = element.text
		if (text.find('Version:') > 0):
			details.append(getVersion(getString(text)))
		if (text.find('Published:') > 0):
			details.append(getString(text))
		if (text.find('License:') > 0):
			details.append(getString(text))
		# For some reason, these last two json elements get caught in "overflow" of the HTML of some packages
		# Explore this more in the future.  For now, just manually research and capture
		if (text.find('Imported by:') > 0):
			details.append(getValue(text))
		if (text.find('Imports:') > 0):
			details.append(getValue(text))
	return details

def getValue(text):
	return int(((text).split(':')[1]).replace(',',''))

def getString(text):
	return ((text).split(':')[1]).replace('\n','').strip()

def getVersion(text):
	return text[:text.index('Latest')]

def getPkgDetailsForMod(mod, ver):
	response = requests.get(PKG_GO_URL+mod)
	content = BeautifulSoup(response.content, 'html.parser')
	try:
		return getDetails(content)
	except:
		return(['go.dev","error getting details'])
	return(entry)

def getRepoBaseData(repo_url):
	response = requests.get(repo_url, headers=HEADERS)
	data = response.json()
	returnData = []
	try:
		returnData.append(data['forks'])
		returnData.append(data['subscribers_count'])  #actually the number of watchers per the UI
		returnData.append(data['stargazers_count'])
	except:
		returnData.append("error getting base data")
	return returnData

def getCountOfAtAPI(repo_url, api):
	more = True
	page = 1
	total = 0
	while more:
		response = requests.get(repo_url+api+'?anon=1&per_page=100&page=' + str(page), headers=HEADERS)
		txt = response.json()
		if len(txt) > 0:
			total = total + len(txt)
			page = page + 1
		else:
			more = False
	return [total]

def getLatestReleaseDate(repo_url, api):
	response = requests.get(repo_url+api, headers=HEADERS)
	data = response.json()
	if len(data) > 0:
		returnData = []
		try:
			lastRelease = data[0]
			returnData.append(lastRelease.get('published_at',"No releases"))
		except:
			returnData.append("error getting last release")
		return returnData
	else:
		return ['None']

def getLastCommitDate(repo_url, api):
	response = requests.get(repo_url+api, headers=HEADERS)
	data = response.json()
	returnData = []
	try:
		lastCommit = data[0]['commit']['committer']['date']
		returnData.append(lastCommit)
	except:
		returnData.append("error getting last commit")
	return returnData


def getRepoData(pkg_url):
	mod_data = pkg_url.replace('github.com/','').split('/')
	owner = mod_data[0]
	repo = mod_data[1]
	base_repo_url = GITHUB_API_URL+owner+'/'+repo
	returnData = []
	returnData.extend(getRepoBaseData(base_repo_url))
	returnData.extend(getCountOfAtAPI(base_repo_url, '/contributors'))
	returnData.extend(getCountOfAtAPI(base_repo_url, '/tags'))
	returnData.extend(getCountOfAtAPI(base_repo_url, '/releases'))
	returnData.extend(getLatestReleaseDate(base_repo_url, '/releases'))
	returnData.extend(getLastCommitDate(base_repo_url,'/commits'))
	return returnData
	
def outputCSV (paperStudy):
	with open ('paper-study.csv','a') as f:
		write = csv.writer(f)
		write.writerow(paperStudy)

GITHUB_API_URL = 'https://api.github.com/repos/'
PKG_GO_URL = 'https://pkg.go.dev/'
AUTH_TOKEN = ''  #to be replaced by your Github authorization token
HEADERS = {
	'Authorization': 'Bearer '+AUTH_TOKEN 
}
DEBUG = True
try:
	outputCSV(['Module','Version Used','Forks','Watchers','Stars','# of Contributors','# of Tags','# of Releases','Last Release Date','Last Commit','Version examined','Published Data','License Type','# of Imported By','# of Imports'])	
	with open('modules.txt','rt') as file:
		for line in file:
			mod = line.split(" ")
			packageURL = mod[0]
			ver = mod[1].replace('\n','')
			if DEBUG:
				print('---> ' + packageURL + ', ver: ' + ver)
			if 'github.com' in packageURL:
				paperStudy = [packageURL, ver]
				paperStudy.extend(getRepoData(packageURL))
				paperStudy.extend(getPkgDetailsForMod(packageURL,ver))
			else:
				paperStudy = [packageURL, ver, 'Non-Github package', 'requires manual review', '','','','','','']
				paperStudy.extend(getPkgDetailsForMod(packageURL,ver))
			if DEBUG:
				print(paperStudy)
			outputCSV(paperStudy)
except:
	print("Problems opening module file or getting any repo data")


