# A scraper which collects the group elements from bilbao

from bs4 import BeautifulSoup
import requests
import re
import numpy as np
from CSV_writer import csvWrite

page_link = 'http://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-getgen'
# this is the url that we've already determined is safe and legal to scrape from.

page_response = requests.post(page_link, data={'gnum': '205', 'list': 'Standard/Default+Setting', 'what': 'gp'} ,timeout=5)
# here, we fetch the content from the url, using the requests library

page_content = BeautifulSoup(page_response.content, "html.parser")
#we use the html parser to parse the url content and store it in a variable.

tr=page_content.find_all("tr")

i=0
while True:
    if i>=len(tr):
        break
    elif(not tr[i].find(id=re.compile('op*'))):
        tr.remove(tr[i])
    else:
        i+=1

content=[]
for r in tr:
    matrix=r.find("pre").text.encode('ascii','ignore')
    ita=r.find_all("td")[6].text.encode('ascii','ignore')
    content.append((ita,matrix))

test=[]
for x in content:
    a=np.fromstring(x[1].replace('\n', '').replace('1/2','0.5').replace('1/4','0.25').replace('3/4','0.75'), sep=" ", dtype=float).reshape(3,4)
    test.append({'ITA': x[0], 'rot': a[:,0:3], 'trans': a[:,3]})

csvWrite('../data/ge/ge205.csv', ['ITA', 'rot', 'trans'], test)