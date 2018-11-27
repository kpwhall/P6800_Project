from CSV_IO import csvRead
from sympy import symbols, sympify, exp, I, pi
from sympy.matrices import Matrix
import os.path

# Parameter definitions ############################
SPACE=int(input("Select a space group: (Only 198,204,205,221 for testing purposes): "))   # Space group being considered

# Collect data on space groups
if os.path.exists("./data/ge/ge"+str(SPACE)+".csv"):
    ge = csvRead("./data/ge/ge"+str(SPACE)+".csv", ['ITA', 'rot', 'trans'])
else:
    print "File not found, Scraper not yet implemented for general case. Exiting"
    exit()
if os.path.exists("./data/wp/wp"+str(SPACE)+".csv"):
    wp = csvRead("./data/wp/wp"+str(SPACE)+".csv", ['Mult', 'Letter', 'Symm', 'Pos'])
else:    
    print "File not found, Scraper not yet implemented for general case. Exiting"
    exit()
if os.path.exists("./data/ct/ct"+str(SPACE)+".csv"):
    ct = csvRead("./data/ct/ct"+str(SPACE)+".csv", ["IR","Char"])
else:    
    print "File not found, Scraper not yet implemented for general case. Exiting"
    exit()

#Serialize transforms. For the purposes of this program, one per class is all that's needed, so we can disregard the rest.
#   This method of getting classes doesn't seem to work. E.g., for Oh symmetry. 4+ and 4- should be in the same class.
transforms=[]
classList=[]
for x in ge:
    if (not x[0].split()[0] in classList):
        classList.append(x[0].split()[0])
        transforms.append([Matrix(sympify(x[1])),Matrix(sympify(x[2])),x[0]])

charIR=[]
charTab=[]
i=0
for t in ct:
    charIR.append(t[0])
    charTab.append([])
    for l in t[1].replace('[','').replace(']','').split(','):
        a=l.replace('{','').replace('}','').replace("'","").split(':')
        charTab[i].append({a[0]: sympify(a[1])})
    i+=1

for i in range(len(charIR)):
    print charIR[i]
    print charTab[i],"\n"

exit()
print "Classes:"
print " ", classList
print " ", ct[1],"\n"

#Serialize all Wyckoff positions. May easily be changed to take only a selected Wyckoff position if required.
pos, ptitle=[],[]
i=0
for x in wp:
    ptitle.append(x[0]+x[1])
    pos.append(i)
    pos[i]=[]
    for y in x[3].split(', '):
        z=y.replace('[M','M').replace(')]',')') # Removes left over braces
        pos[i].append(Matrix(sympify(z)))
    i+=1

for i in range(len(ptitle)):
    print ptitle[i]
    for j in pos[i]:
        print " ", j
print 

# Atomic character
i=0
achar=[]
for x in pos:
    achar.append([])
    for t in transforms:
        count=0
        for y in x:
            if t[0]*y+t[1]==y:
                count+=1
        achar[i].append(count)
    i+=1
    

# Displacement character
vec=Matrix(sympify("[[x],[y],[z]]"))
dchar=[]
i=0
for t in transforms:
    count=0
    tvec=t[0]*vec+t[1]
    for i in range(3):
        count += 1 if tvec[i]==vec[i] else 0
        count -= 1 if tvec[i]==-vec[i] else 0
    dchar.append(count)

#characters
char=[]
print " ", classList
for i in range(len(ptitle)):
    char.append([])
    for j in range(len(achar[i])):
        char[i].append(achar[i][j]*dchar[j])
    print ptitle[i],char[i]