# bilbao_ge_scraper collects the Character tables and associated data from bilbao
#
from bs4 import BeautifulSoup       # BeautifulSoup for parsing of html.
import requests, re                 # Requests for POST/GET requests. Re for regex.
from sympy import symbols, sympify  # SymPy for symbolic mathematics.
from sympy.matrices import Matrix   #
from CSV_IO import csvWrite         # csvWrite from CSV_IO.py.

# Parameter definitions ############################
SPACE=199                                                               # Space group
page_link = 'http://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-getgen' # URL to scrape from

# Collect page data
#   Send page request and parse html data using BeautifulSoup
page_response = requests.post(page_link, data={'gnum': str(SPACE), 'list': 'Standard/Default+Setting', 'what': 'gp'} ,timeout=10)
page_content = BeautifulSoup(page_response.content, "html.parser")

# Parse data to collect what we need.
#
while page_content.find('tbody'):
    page_content.find('tbody').decompose()  # Destroy first <tbody> tag
tr=page_content.find_all("tr")

i=0
while True:
    if i>=len(tr):
        break
    elif(not tr[i].find(id=re.compile('^op[0-9]+'))):   # Remove rows that don't have an id op#
        tr.remove(tr[i])
    else:
        i+=1

content=[]
for r in tr:    # Go row by row and convert the strings to matrices
    matrix="[["+r.find('pre').text.encode('ascii','ignore').strip().replace('  ', ',').replace('\n','],[').replace(' ',',').replace(',,',',').replace('[,','[')+"]]"
    ita=r.find_all("td")[6].text.encode('ascii','ignore')   # Get ITA name
    content.append((ita,matrix))

# Serialise collected data for storage
#   Then write to csv file
data=[] # List to hold data as series of dicts
for x in content:
    a=Matrix(sympify(x[1]))
    data.append({'ITA': x[0], 'rot': a[:,0:3], 'trans': a[:,3]})
csvWrite('../data/ge/ge'+str(SPACE)+'.csv', ['ITA', 'rot', 'trans'], data) 