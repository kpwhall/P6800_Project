# A scraper which collects the group elements from bilbao

from bs4 import BeautifulSoup
import requests

page_link = 'http://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-getgen'
# this is the url that we've already determined is safe and legal to scrape from.

page_response = requests.post(page_link, data={'gnum': '205', 'list': 'Standard/Default+Setting', 'what': 'gp'} ,timeout=5)
# here, we fetch the content from the url, using the requests library

page_content = BeautifulSoup(page_response.content, "html.parser")
#we use the html parser to parse the url content and store it in a variable.

textContent = []
content= page_content.find_all("pre")

for x in content:
    paragraphs = x.text
    textContent.append(paragraphs)

c=1
for i in textContent:
    print c
    print i + "\n"
    c+=1