# coding=UTF-8
import csv
import socket
import requests
#import pandas as pd
import lxml
from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import diff_match_patch as dmp_module

def scrape(presidents_url):
	all_names = []
	page_html_text = requests.get(presidents_url).text
	page_html = fromstring(page_html_text)
	links = page_html.cssselect(".wikitable big a")
	for link in links:
		all_names.append(link.get('href').replace("/wiki/",""))


	urls = []
	wiki_presidents_url = []
	infogalactic_presidents_url = []
	for name in all_names:
		urls.append("https://infogalactic.com/w/index.php?title=" + name + "&action=history")

	
	browser = webdriver.Chrome()

	user_agent = "Chrome/76.0.3809.132"
	headers = {'User-Agent': user_agent}

	for i in range(len(urls)):
		browser.implicitly_wait(10)
		browser.get(urls[i])

		response = requests.get(urls[i], headers=headers).text
		history_html = fromstring(response)

		revisions = history_html.cssselect("#pagehistory li")
		print("%s: %d" % (all_names[i], len(revisions)))

		if len(revisions) > 1:
			wiki_presidents_url.append("https://en.wikipedia.org/wiki/" + all_names[i])
			infogalactic_presidents_url.append("https://infogalactic.com/info/" + all_names[i])

	for i in range(len(wiki_presidents_url)):
		browser.implicitly_wait(10)
		browser.get(wiki_presidents_url[i])

		wiki_text = ""
		info_text = ""

		response = requests.get(wiki_presidents_url[i], headers=headers).text
		if '<h2>' in response:
			response = response.partition("<h2>")[0]
		wiki_html = fromstring(response)
		all_wiki_text = wiki_html.cssselect(".mw-parser-output p:not(.mw-empty-elt)")
		for text in all_wiki_text:
			wiki_text += text.text_content().strip() + '\n'

		browser.implicitly_wait(10)
		browser.get(infogalactic_presidents_url[i])

		response = requests.get(infogalactic_presidents_url[i], headers=headers).text
		if '<h2>' in response:
			response = response.partition("<h2>")[0]
		info_html = fromstring(response)
		all_info_text = info_html.cssselect("#mw-content-text >p")
		for text in all_info_text:
			info_text += text.text_content().strip() + '\n'


		dmp = dmp_module.diff_match_patch()
		dmp.Diff_Timeout = 0
		diff = dmp.diff_main(wiki_text, info_text)

		dmp.diff_cleanupSemantic(diff)

		string = dmp.diff_prettyHtml(diff)

		# string = ""

		# for diff_tuple in diff:
		# 	if diff_tuple[0] == 1:
		# 		string += "<span class='blue'>" + diff_tuple[1] + "</span>"
		# 	elif diff_tuple[0] == -1:
		# 		string += "<span class='red'>" + diff_tuple[1] + "</span>"
		# 	else:
		# 		string += diff_tuple[1]
		# 	if '\n' in diff_tuple[1]:
		# 		string += "<br><br>"

		president_name = wiki_presidents_url[i].replace("https://en.wikipedia.org/wiki/","")
		filename = president_name + ".html"
		f = open(filename,'w', encoding='UTF-8')

		wrapper = """<html>
		<head>
		<title>%s</title>
		</head>
		<body><p>%s</p></body>
		</html>"""

		whole = wrapper % (president_name, string)
		f.write(whole)
		f.close()



if __name__ == '__main__':
	presidents_url = "https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"
	scrape(presidents_url)
