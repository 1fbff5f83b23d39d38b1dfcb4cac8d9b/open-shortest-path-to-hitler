import urllib2, re, Queue, threading, time, collections
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup, SoupStrainer

Q = Queue.Queue() #Sky's the limit! (Along with memory)
baseurl = "https://en.wikipedia.org"
initial_link = "https://en.wikipedia.org/wiki/Charles_Whitman"
finish_link = "https://en.wikipedia.org/wiki/Adolf_Hitler"

#pathing works by making (origin, link) tuples and then searching through them once hitler is found, and linking tuples where (origin, link = origin, link)
#link: link found in origin
#origin: origin of found link 
#(I hope this cleared everything up)
#rec_depth: How many links deep in we are (does not work)
#path: list of (origin, link) tuples
#path_the_second: stupid name for the path taken

def pretty_print(path):
	global link_num
	print "Checked "+str(link_num)+" links in "+str(int(time.time() - time_start))+" seconds"
	print initial_link.lower()
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
	global link_num
	link, rec_depth, origin, path = Q.get()
	try:
		print "Last indexed page: "+link
		print "Recursion depth:   "+str(rec_depth) 
		path.append((origin, link))
		origin = link
		if rec_depth >= 2: return #broken, I guess?
		page = urllib2.urlopen(link).read()
		for link in BeautifulSoup(page, parseOnlyThese=SoupStrainer('a')):
			if link.has_key('href'):
				link_num += 1
				link = link['href']
				if link in history: continue
				if link.startswith("#"): continue
				if "file:" in link.lower() or "help:" in link.lower(): continue
				if "wikipedia:" in link.lower() or "category:" in link.lower(): continue
				if "special:" in link.lower() or "talk:" in link.lower(): continue
				if not "wiki" in link.lower(): continue
				if not link.startswith("http"):
					if not link.lower().startswith("/wiki/"): continue
					link = urljoin(baseurl, link)
				if not "en.wikipedia.org" in link.lower(): continue
				if link.lower() == finish_link:
					print "Hitler found! Now constructing path."
					path.append((origin, link))
					path_the_second = [path[-1]]
					get_path(origin, link, path_the_second, path)
					exit()
				Q.put_nowait((link, rec_depth+1, origin, path)) #nowait so it doesn't hang up if it runs out of queue space
	except Exception as e:
		print e
		return
		
global link_num
link_num = 0
time_start = time.time()
history = collections.deque([])
Q.put((initial_link, 0, initial_link, []))
while True:
	if not Q.qsize(): break
	print "Queue size: "+str(Q.qsize())
	print "Indexed "+str(link_num)+" pages."
	get_links()