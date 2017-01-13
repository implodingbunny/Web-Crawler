# Run on Python 3.5
import sys
import urllib.request
import urllib.parse
import re

# Enter URL to crawl and then add them to a set of unvisited (and make an empty set of visited to initialise)
startUrl = input("Please enter a URL to crawl: ")
if (re.match('(?:http|ftp|https)://', startUrl) == None):
	startUrl = "http://" + startUrl
unvisitedUrls = set([])
unvisitedUrls.add(startUrl)
visitedUrls = set([])

# Strip tags from links
tagregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')

while True:
	# Gets a new URL from the list
	try:
		currentUrl = unvisitedUrls.pop()
	# Throw exception if set empty
	except KeyError:
		print("----- Finished searching -----")
		raise StopIteration
	url = urllib.parse.urlparse(currentUrl)
	domain = startUrl.split("://",1)[1]

	# Check to ensure the link is within the same domain
	if(url.netloc==domain):
		try:
			resp = urllib.request.urlopen(currentUrl)
		except:
			continue

		# Search for the title tag and its contents
		msg = str(resp.read())
		start = msg.find('<title>')
		if (start >= 0):
			end = msg.find('</title>', start+7)
			title = msg[start+7:end]
			print(title)
			print(currentUrl)
			print("Links:")

		# Search for links in page
		links = tagregex.findall(msg)

		# Add correctly formatted links to set for looping
		visitedUrls.add(currentUrl)
		for link in (links.pop(0) for _ in range(len(links))):
			if link.startswith('/'):
				link = 'http://' + url[1] + link
			elif link.startswith('#'):
				link = 'http://' + url[1] + url[2] + link
			elif not link.startswith('http'):
				link = 'http://' + url[1] + '/' + link
			linkDomain = urllib.parse.urlparse(link).netloc
			if(linkDomain==domain):
				if (link not in visitedUrls):
					unvisitedUrls.add(link)
				print("- " + link)
		print()
