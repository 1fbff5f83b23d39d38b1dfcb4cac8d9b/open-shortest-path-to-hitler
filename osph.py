import urllib2, re, Queue, threading
from BeautifulSoup import BeautifulSoup, SoupStrainer

q = Queue.Queue(1000)

def get_links(link, rec_depth, path):
	try:
		#path.append(link)
		if "hitler" in link.lower(): print link
		if link.lower() == "https://en.wikipedia.org/wiki/adolf_hitler" or link.lower() == "http://en.wikipedia.org/wiki/adolf_hitler": exit(path)
		if rec_depth >= 2: return
		page = urllib2.urlopen(link).read()
		for link in BeautifulSoup(page, parseOnlyThese=SoupStrainer('a')):
			if link.has_key('href'):
				get_links("https://en.wikipedia.org"+link['href'], rec_depth+1, path)
	except Exception as e:
		print e
		return
		
get_links("https://en.wikipedia.org/wiki/Auschwitz_concentration_camp", 0, [])