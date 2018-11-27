from CSV_IO import csvRead
from sympy import symbols, sympify
from sympy.matrices import Matrix

# Parameter definitions ############################
SPACE=204   # Space group being considered

# Collect data on space groups
ge = csvRead("./data/ge/ge"+str(SPACE)+".csv", ['ITA', 'rot', 'trans'])
wp = csvRead("./data/wp/wp"+str(SPACE)+".csv", ['Mult', 'Letter', 'Symm', 'Pos'])

#Get transforms. For the purposes of this program, one per class is all that's needed, so we can disregard the rest.
transforms=[]
classList=[]
for x in ge:
    if (not x[0].split()[0] in classList):
        classList.append(x[0].split()[0])
        transforms.append([Matrix(sympify(x[1])),Matrix(sympify(x[2])),x[0]])

#Get all Wyckoff positions. May easily be changed to take only a selected Wyckoff position if required.
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
for i in range(len(ptitle)):
    print ptitle[i]
    char.append([])
    for j in range(len(achar[i])):
        char[i].append(achar[i][j]*dchar[j])
    print char[i]
    print

myset=[]
for i in transforms:
    myset.append(i[2].split()[0])

print list(set(myset))