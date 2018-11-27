# A scraper which collects the Wyckoff positions from bilbao

from bs4 import BeautifulSoup
import requests, re
from sympy import symbols, sympify
from sympy.matrices import Matrix
from CSV_IO import csvWrite

x,y,z=symbols('x y z')

page_link = 'http://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-wp-list'
# this is the url that we've already determined is safe and legal to scrape from.

page_response = requests.post(page_link, data={'gnum': '205', 'list': 'Standard/Default+Setting'} ,timeout=10)
# here, we fetch the content from the url, using the requests library

page_content = BeautifulSoup(page_response.content, "html.parser")
#we use the html parser to parse the url content and store it in a variable.

tr=page_content.find_all("tr")

i=0
while True:
    if i>=len(tr):
        break
    elif((not tr[i].find("td",{"align": "center"})) or (not tr[i].find("nobr"))):
        tr.remove(tr[i])
    else:
        i+=1
# tr=tr[::2]

content, text=[],[]
mult,letter,symm=None,None,None
for r in tr:
    if r.find("table"):
        content.append((mult,letter,symm,text))
        text=[]
        td=r.find_all("td")
        mult=td[0].text.encode('ascii','ignore')
        letter=td[1].text.encode('ascii','ignore')
        symm=td[2].text.encode('ascii','ignore')
    nobr=r.find_all("nobr")
    for n in nobr:
        tx=n.text.encode('ascii','ignore')
        text.append(Matrix(sympify(tx)))
content.append((mult,letter,symm,text))
content.pop(0)  #Remove the first, null element from the content list

data=[]
for x in content:
    data.append({'Mult': x[0], 'Letter': x[1], 'Symm': x[2], 'Pos': x[3]})

csvWrite('../data/wp/wp205.csv', ['Mult', 'Letter', 'Symm', 'Pos'], data)