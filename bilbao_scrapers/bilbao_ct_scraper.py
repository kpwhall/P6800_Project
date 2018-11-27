# A scraper which collects the Character tables from bilbao
#

from bs4 import BeautifulSoup
import requests, re
from sympy import symbols, sympify
from sympy.matrices import Matrix
from CSV_IO import csvWrite

SPACE=221
x,y,z=symbols('x y z')

page_link = 'http://www.cryst.ehu.es/cgi-bin/rep/programs/sam/point.py?sg='+str(SPACE)+'&num=0'
# this is the url that we've already determined is safe and legal to scrape from.

page_response = requests.get(page_link ,timeout=10)
# here, we fetch the content from the url, using the requests library

page_content = BeautifulSoup(page_response.content, "html.parser")
#we use the html parser to parse the url content and store it in a variable.

tab=page_content.find("table",{"border": "2"})
tr=tab.find_all("tr")

fr=tr.pop(0)
fd=fr.find_all("td")
fd=fd[2:len(fd)-1]
cls=[]
for d in fd:
    cls.append(d.text.encode('ascii','ignore'))

if tr[0].find("nobr").text=="Mult.": 
    tr.pop(0)

content=[]
for r in tr:
    char=[]
    td=r.find_all("td")
    if td[0].find("sup"):
        name=[]
        name.append(td[0].text[:3].encode('ascii','ignore'))
        name.append(td[0].text[3:].encode('ascii','ignore'))
        char.append([])
        char.append([])
        for i in range(len(td)-3):
            string=str(td[i+2].find("nobr"))
            string=string.replace('<sup>','').replace('</sup>','').replace('<nobr>','').replace('</nobr>','')
            string=string.replace('w2','exp(-2 i Pi/3)').replace('w','exp(2 i Pi/3)').split('<br/>')    # Does it have to be w=exp(2 i pi/3)?
            char[0].append({cls[i]: string[0]})
            char[1].append({cls[i]: string[1]})
        for i in range(2):
            content.append((name[i],char[i]))
    else:
        name=td[0].text.encode('ascii','ignore')
        for i in range(len(td)-3):
            string=str(td[i+2].find("nobr"))
            string=string.replace('<sup>','').replace('</sup>','').replace('<nobr>','').replace('</nobr>','')
            string=string.replace('w2','exp(-2 i Pi/3)').replace('w','exp(2 i Pi/3)')
            char.append({cls[i]: string})
        content.append((name,char))

data=[]
for x in content:
    data.append({"IR": x[0], "Char": x[1]})

csvWrite('../data/ct/ct'+str(SPACE)+'.csv', ["IR","Char"], data)