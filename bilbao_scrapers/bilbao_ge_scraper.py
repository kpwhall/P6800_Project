# A scraper which collects the group elements from bilbao

from bs4 import BeautifulSoup
import requests, re
from sympy import symbols, sympify
from sympy.matrices import Matrix
from CSV_IO import csvWrite

SPACE=199

page_link = 'http://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-getgen'
# this is the url that we've already determined is safe and legal to scrape from.

page_response = requests.post(page_link, data={'gnum': str(SPACE), 'list': 'Standard/Default+Setting', 'what': 'gp'} ,timeout=10)
# here, we fetch the content from the url, using the requests library

page_content = BeautifulSoup(page_response.content, "html.parser")
#we use the html parser to parse the url content and store it in a variable.

while page_content.find('tbody'):
    page_content.find('tbody').decompose()
tr=page_content.find_all("tr")

i=0
while True:
    if i>=len(tr):
        break
    elif(not tr[i].find(id=re.compile('^op[0-9]+'))):
        tr.remove(tr[i])
    else:
        i+=1

content=[]
for r in tr:
    matrix="[["+r.find('pre').text.encode('ascii','ignore').strip().replace('  ', ',').replace('\n','],[').replace(' ',',').replace(',,',',').replace('[,','[')+"]]"
    ita=r.find_all("td")[6].text.encode('ascii','ignore')
    content.append((ita,matrix))

data=[]
for x in content:
    # a=np.fromstring(x[1].replace('\n', '').replace('1/2','0.5').replace('1/4','0.25').replace('3/4','0.75'), sep=" ", dtype=float).reshape(3,4)
    a=Matrix(sympify(x[1]))
    data.append({'ITA': x[0], 'rot': a[:,0:3], 'trans': a[:,3]})

csvWrite('../data/ge/ge'+str(SPACE)+'.csv', ['ITA', 'rot', 'trans'], data)