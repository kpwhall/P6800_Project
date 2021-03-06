# bilbao_ct_scraper collects the Character tables and associated data from bilbao
#
from bs4 import BeautifulSoup   # BeautifulSoup allows parsing of html.
import requests                 # Requests for POST/GET requests.
from CSV_IO import csvWrite     # csvWrite from CSV_IO.py.

# Parameter definitions ############################
SPACE=199                                                                                       # Space group
page_link='http://www.cryst.ehu.es/cgi-bin/rep/programs/sam/point.py?sg='+str(SPACE)+'&num=0'   # URL to scrape from

# Collect page data
#   Send page request and parse html data using BeautifulSoup
page_response=requests.get(page_link ,timeout=10)
page_content=BeautifulSoup(page_response.content, "html.parser")

# Parse and serialise data
#   Parse html data line by line to collect required data.
tab=page_content.find("table",{"border": "2"})  # Collect first <table> with attribute border=2
tr=tab.find_all("tr")                           # Collect all <tr> within tab

fr=tr.pop(0)            # Take first row in tr and store it in a new variable
fd=fr.find_all("td")    #   and collect the class names from it.
fd=fd[2:len(fd)-1]
cls=[]                  # cls is a list that stores class names.
for d in fd:
    cls.append(d.text.encode('ascii','ignore'))

if tr[0].find("nobr").text=="Mult.":    # Remove IR: Mult.
    tr.pop(0)

content=[]
for r in tr:
    char=[]
    td=r.find_all("td")
    if td[0].find("sup") and (not '\'' in td[0].find("sup").text):
        name=[]
        name.append(td[0].text[:len(td[0].text)/2].encode('ascii','ignore'))
        name.append(td[0].text[len(td[0].text)/2:].encode('ascii','ignore'))
        char.append([])
        char.append([])
        for i in range(len(td)-3):
            string=str(td[i+2].find("nobr"))
            string=string.replace('<sup>','').replace('</sup>','').replace('<nobr>','').replace('</nobr>','')
            string=string.replace('w2','exp(-2*I*pi/3)').replace('w','exp(2*I*pi/3)').split('<br/>')
            char[0].append({cls[i]: string[0]})
            char[1].append({cls[i]: string[1]})
        for i in range(2):
            content.append((name[i],char[i]))
    else:
        name=td[0].text.encode('ascii','ignore')
        for i in range(len(td)-3):
            string=str(td[i+2].find("nobr"))
            string=string.replace('<sup>','').replace('</sup>','').replace('<nobr>','').replace('</nobr>','')
            string=string.replace('w2','exp(-2*I*pi/3)').replace('w','exp(2*I*pi/3)')
            char.append({cls[i]: string})
        content.append((name,char))

# Collect data for storage
#   Then write to csv file
data=[] # List to hold data as series of dicts
for x in content:
    data.append({"IR": x[0], "Char": x[1]})
csvWrite('../data/ct/ct'+str(SPACE)+'.csv', ["IR","Char"], data)