import urllib2, re, Queue, threading

q = Queue.Queue(1000)

def get_links(link, rec_depth, path):
	try:
		path.append(link)
		if link == "https://en.wikipedia.org/wiki/Adolf_Hitler" or link == "http://en.wikipedia.org/wiki/Adolf_Hitler": exit(path)
		if rec_depth >= 4: return
		page = urllib2.urlopen(link).read()
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', page)
		for link in urls:
			print link
			get_links(link, rec_depth+1, path)
	except Exception as e: 
		print e
		return
		
get_links("https://en.wikipedia.org/wiki/Auschwitz_concentration_camp", 0, [])