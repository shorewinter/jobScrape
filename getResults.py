import bs4
import urllib.request
import demjson
import csv
import time

page = 0
pages = 1
jobs = []
while page != pages:
	url = 'https://www.seek.co.nz/jobs-in-information-communication-technology/in-All-Auckland?page=' + str(page) + '&sortmode=ListedDate'
	print(url)
	req = urllib.request.Request(
		url,
		data=None,
		headers={
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'en-US,en;q=0.8',
		'Connection': 'keep-alive'
		}
	)

	get = urllib.request.urlopen(req)
	html = get.read().decode('utf-8')
	soup = bs4.BeautifulSoup(html, 'html.parser')

	if page == 0:
		pages = soup.find('strong', {'data-automation': 'totalJobsCount'})
		pages = pages.get_text().strip()
		pages = int(int(pages) / 19 - 1)
		print(pages)
	soup = soup.find('script', {'data-automation': 'server-state'})
	data = soup.prettify().split('window.SEEK_REDUX_DATA = ')[1].split(';\n')[0]
	obj = demjson.decode(data)
	jobs.append(obj['results']['results']['jobs'])

	page += 1
	time.sleep(1)
f = open("test.csv", "w", newline='', encoding='utf-8')
keys = jobs[0][0].keys()
w = csv.DictWriter(f, keys, extrasaction='ignore')
w.writeheader()
for i in range(len(jobs)):
	w.writerows(jobs[i])
f.close()