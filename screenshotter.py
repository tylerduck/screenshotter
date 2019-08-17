from urllib.request import urlopen
from bs4 import BeautifulSoup
from lxml import html
import urllib
import imgkit
from time import sleep
import sys
import pickle

def remove_last_slash(S):
	if S[-1] == "/":
		return S[:-1]
	return S

def get_links_on_page(base_url, curr):
	links = []
	try:
		page = urlopen(curr)
	except urllib.error.HTTPError:
		return []

	soup = BeautifulSoup(page, "html.parser")

	base_url = remove_last_slash(base_url)
	curr = remove_last_slash(curr)

	#links = soup.find_all('a',href=True)

	for link in soup.find_all('a',href=True):
		the_link = link['href']
		if the_link != "":
			if base_url in the_link:
				links.append(the_link)
			elif the_link[0] == "/":
				links.append(base_url + the_link)
	return links

def check_link(link):
	return "?" not in link and "#" not in link

def get_all_links(base_url, curr_url, directory, visited=[]):
	sys.stdout.write("\rLinks Found: %d" % len(visited))
	sys.stdout.flush()
	sleep(2)
	visited.append(curr_url)
	d = directory + ".picklerick"
	pickle.dump(visited, open(d, "wb"))
	try:
		sub_links = get_links_on_page(base_url, curr_url)
		# remove anchor and query links
		sub_links = [link for link in sub_links if check_link(link)]
		sub_links = list(set(sub_links) - set(visited))
		for s in sub_links:
			assert s not in visited 
	except:
		sub_links = []
		visited.remove(curr_url)
	for link in sub_links:
		get_all_links(base_url, link, directory, visited)
	return visited

def remove_extension(S):
	return S.split(".")[0]

def collect_png(site, save_dir, option=0):
	try:
		pages = pickle.load( open(save_dir + ".picklerick", "rb" ) )
		page = pages[-1]
	except:
		pages = []
		page = site
	if option == 0:
		links = get_all_links(site, page, save_dir, pages)
	elif option ==1:
		links = get_links_on_page(site, site)
	else:
		links = [site]
	
	for link in links:
		if link == site:
			filename = save_dir + "/home.png"
		else:
			n = save_dir[-1] == "/"
			if link[-1] == "/": link = link[:-1]
			filename = save_dir + remove_extension(link[link.rfind("/") + n:]) + ".png"
		try:
			options = {'format': 'png', 'width': 1080, 'disable-smart-width': ''}
			imgkit.from_url(link, filename, options = options)
		except:
			pass


collect_png("https://www.wish-bone.com", "/home/tyler/Documents/WishBone/")
# pages = pickle.load( open("/home/tyler/Documents/WishBone/" + "save.p", "rb" ) )
# print(pages)

# l = [1,2,3,4]
# subl = [1,7]
# print(list(set(subl) - set(l)))