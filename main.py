from CSV_IO import csvRead
from sympy import symbols, sympify, exp, I, pi, solve_linear_system, simplify
from sympy.matrices import Matrix
import os.path

# Parameter definitions ############################
SPACE=int(input("Select a space group: (Only 198,204,205,221 for testing purposes): "))   # Space group being considered
x,y,z=symbols('x y z')

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
for g in ge:
    if (not g[0].split()[0] in classList):
        classList.append(g[0].split()[0])
        transforms.append([Matrix(sympify(g[1])),Matrix(sympify(g[2])),g[0]])

#Serialize character table
charIR,charTab=[],[]
i=0
for t in ct:
    charIR.append(t[0])
    charTab.append([])
    for l in t[1].replace('[','').replace(']','').split(','):
        a=l.replace('{','').replace('}','').replace("'","").split(':')
        charTab[i].append({"Class": a[0].strip(), "Value": sympify(a[1])})
    i+=1

for i in range(len(charIR)):
    class_map = {c['Class']: c for c in charTab[i]}
    charTab[i] = [class_map[id]["Value"] for id in classList]

print "Classes:"
print classList

#Serialize all Wyckoff positions. May easily be changed to take only a selected Wyckoff position if required.
pos, ptitle=[],[]
i=0
for a in wp:
    ptitle.append(a[0]+a[1])
    pos.append(i)
    pos[i]=[]
    for b in a[3].split(', '):
        c=b.replace('[M','M').replace(')]',')') # Removes left over braces
        pos[i].append(Matrix(sympify(c)))
    i+=1

# Atomic character
# need to updated to move things back into the cell.
i=0
achar=[]
subZero=[(x,0),(y,0),(z,0)]
for a in pos:
    achar.append([])
    for t in transforms:
        count=0
        for b in a:
            c=t[0]*b+t[1]
            if not (c in a):    # If outside of cell, place inside. THIS DOESN'T WORK FOR 204 BECAUSE I ONLY HAVE HALF of the WYCKOFF positions. Also need all positions + 1/2,1/2,1/2!
                d=c.subs(subZero)
                for j in range(len(d)):
                    c[j]=c[j]-1 if d[j]>=1 else c[j]
                    c[j]=c[j]+1 if d[j]<0 else c[j]
            if c==b:
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
    char.append([])
    for j in range(len(achar[i])):
        char[i].append(achar[i][j]*dchar[j])
    print ptitle[i]
    print "Atomic character:       ", achar[i]
    print "Displacement character: ", dchar
    print "Total character:        ", char[i]
print

systemSeed=Matrix()
for r in charTab:
    systemSeed=systemSeed.col_insert(len(systemSeed)/len(r),Matrix(r))   # Need to ensure the columns are lined up correctly.

a=symbols('a0:'+str(len(charTab[0])))

# a,b,c,d,e,f,g,h=symbols('a,b,c,d,e,f,g,h') # How to make this general? It won't accept the above.

for i in range(len(ptitle)):
    system=systemSeed.col_insert(len(charTab[i]),Matrix(char[i]))
    # ss=solve_linear_system(system,a[0],a[1],a[2],a[3])
    ss=solve_linear_system(system,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7])
    for j in a:
        ss[j]=ss[j].expand(complex=True)
    print ptitle[i], ss

#So, solve will accept a list of values, but solve_linear_system will not. Bummer.
# Why are there fractions?
# I forgot to pull things back inside the unit cell. That could explain it!


