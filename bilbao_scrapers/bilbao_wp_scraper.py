# A scraper which collects the Wyckoff positions from bilbao
#
from bs4 import BeautifulSoup       # BeautifulSoup for parsing of html.
import requests                     # Requests for POST/GET requests.
from sympy import symbols, sympify  # SymPy for symbolic mathematics.
from sympy.matrices import Matrix   #
from CSV_IO import csvWrite         # csvWrite from CSV_IO.py.

# Parameter definitions ############################
SPACE=199                                                                   # Space group
x,y,z=symbols('x y z')                                                      # Set x, y, z as symbols for sympy symbolic computation
page_link = 'http://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-wp-list'    # URL to scrape from

# Collect page data
#   Send page request and parse html data using BeautifulSoup
page_response = requests.post(page_link, data={'gnum': str(SPACE), 'list': 'Standard/Default+Setting'} ,timeout=10)
page_content = BeautifulSoup(page_response.content, "html.parser")

# Parse data to collect what we need.
#
tr=page_content.find_all("tr")
shift=[]
for c in tr[2].text.encode('ascii','ignore').split("+")[1:-1]:  # Collect shifts from 3rd row
    shift.append(Matrix(sympify(c.strip().replace("(","").replace(")",""))))

i=0
while True:     # Remove all rows that do not contain needed information
    if i>=len(tr):
        break
    elif((not tr[i].find("td",{"align": "center"})) or (not tr[i].find("nobr"))):
        tr.remove(tr[i])
    else:
        i+=1

content, pos=[],[]
subZero=[(x,0),(y,0),(z,0)]
mult,letter,symm=None,None,None
for r in tr:                # Go row by row
    if r.find("table"):
        content.append((mult,letter,symm,pos))
        pos=[]
        td=r.find_all("td")                         # Find all name information and collect it
        mult=td[0].text.encode('ascii','ignore')
        letter=td[1].text.encode('ascii','ignore')
        symm=td[2].text.encode('ascii','ignore')
    nobr=r.find_all("nobr")                         # Find all positions and collect them
    for n in nobr:
        tx=n.text.encode('ascii','ignore')
        a=Matrix(sympify(tx))
        pos.append(a)    

content.append((mult,letter,symm,pos))
content.pop(0)  #Remove the first, null element from the content list

# Serialise collected data for storage
#   Then write to csv file
data=[]
data.append({'Mult': shift})
for x in content:
    data.append({'Mult': x[0], 'Letter': x[1], 'Symm': x[2], 'Pos': x[3]})
csvWrite('../data/wp/wp'+str(SPACE)+'.csv', ['Mult', 'Letter', 'Symm', 'Pos'], data)