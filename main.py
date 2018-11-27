from CSV_IO import csvRead
from sympy import symbols, sympify
from sympy.matrices import Matrix

# Parameter definitions ############################
SPACE=204   # Space group being considered

# Collect data on space groups
ge = csvRead("./data/ge/ge"+str(SPACE)+".csv", ['ITA', 'rot', 'trans'])
wp = csvRead("./data/wp/wp"+str(SPACE)+".csv", ['Mult', 'Letter', 'Symm', 'Pos'])

rots, trans=[], []
for x in ge:
    rots.append(Matrix(sympify(x[1])))
    trans.append(Matrix(sympify(x[2])))

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

for x in pos:
    print x
    print