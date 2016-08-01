import urllib2, re, Queue, threading
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup, SoupStrainer

Q = Queue.Queue(50000)
baseurl = "https://en.wikipedia.org"
beginning_link = "https://en.wikipedia.org/wiki/Charles_Whitman"

def pretty_print(path):
	print "Checked "+str(Q.qsize())+" links."
	print beginning_link.lower()
	for tuple in path:
		print tuple[1]
	exit()

def get_path(origin, link, path_the_second, path):
	if origin == link:
		path_the_second.pop()
		pretty_print(list(reversed(path_the_second)))
	for tuple in path:
		if tuple[1] == origin:
			path_the_second.append(tuple)
			get_path(tuple[0], tuple[1], path_the_second, path)
			return

def get_links():
	link, rec_depth, origin, path = Q.get()
	try:
		print "Recursion depth: "+str(rec_depth)
		path.append((origin, link))
		origin = link
		if rec_depth >= 2: return
		page = urllib2.urlopen(link).read()
		for link in BeautifulSoup(page, parseOnlyThese=SoupStrainer('a')):
			if link.has_key('href'):
				link = link['href']
				link = link.lower()
				if link.startswith("#"): continue
				if "file:" in link or "help:" in link: continue
				if not link.startswith("http"):
					link = urljoin(baseurl, link)
				
				if link == "https://en.wikipedia.org/wiki/adolf_hitler" or link == "http://en.wikipedia.org/wiki/adolf_hitler":
					path.append((origin, link))
					path_the_second = [path[-1]]
					get_path(origin, link, path_the_second, path)
					exit()
				Q.put_nowait((link, rec_depth+1, origin, path))
	except Exception as e:
		print e
		return
		
Q.put((beginning_link, 0, beginning_link, []))
for i in range(5000):
	if not Q.qsize(): break
	print "Queue size: "+str(Q.qsize())
	get_links()