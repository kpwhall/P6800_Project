from CSV_IO import csvRead                      # csvRead from CSV_IO.py
from sympy import symbols, sympify, exp, I, \
                    pi, solve_linear_system     # SymPy for symbolic mathematics.
from sympy.matrices import Matrix               #
import os.path                                  # os.path for filepath checking.

# Parameter definitions ############################
SPACE=int(input("Select a space group: "))  # Space group being considered
x,y,z=symbols('x y z')                      # Set x, y, z as symbols for sympy symbolic computation

# Collect data on space groups
#   In each case, first check that the file you are looking for exists.
#       If they exist read in the data.
#       If they don't exist, exit.
if os.path.exists("./data/ge/ge"+str(SPACE)+".csv"):
    ge = csvRead("./data/ge/ge"+str(SPACE)+".csv", ['ITA', 'rot', 'trans'])             # Read in Group Element data from .csv file
else:
    print "File not found. Scraper not yet implemented for general case. Exiting"
    exit()
if os.path.exists("./data/wp/wp"+str(SPACE)+".csv"):
    wp = csvRead("./data/wp/wp"+str(SPACE)+".csv", ['Mult', 'Letter', 'Symm', 'Pos'])   # Read in Wyckoff Position data from .csv file
else:    
    print "File not found. Scraper not yet implemented for general case. Exiting"
    exit()
if os.path.exists("./data/ct/ct"+str(SPACE)+".csv"):
    ct = csvRead("./data/ct/ct"+str(SPACE)+".csv", ["IR","Char"])                       # Read in Character Table data from .csv file
else:    
    print "File not found. Scraper not yet implemented for general case. Exiting"
    exit()

# Deserialise group element data
#   Take each group element in the data and convert it to a form usable by this code.
#   Collect classes and a single group element from each class by only considering the first part of the name.
#       This method of getting classes doesn't work in all cases as there isn't a 1:1 correlation between element names and class names
#
transforms,classList=[],[]  # transforms Contains list of group elements as a list [Rotation, Transform, Name]    
                            # classList Contains (incorrect, see above) list of classes
for g in ge:
    if (not g[0].split()[0] in classList):
        classList.append(g[0].split()[0])
        transforms.append([Matrix(sympify(g[1])),Matrix(sympify(g[2])),g[0]])

# Deserialise character table data
#   Take each element of the character tables from data and convert to a form usable by this code.
#
charIR,charTab=[],[]    # charIR contains list of IR names
                        # charTab contains list of characters
i=0                     # Iterator
for t in ct:
    charIR.append(t[0])             
    charTab.append([])
    for l in t[1].replace('[','').replace(']','').split(','):
        a=l.replace('{','').replace('}','').replace("'","").split(':')
        charTab[i].append({"Class": a[0].strip(), "Value": sympify(a[1])})
    i+=1

# Sort charTab to match ordering in classList
#
for i in range(len(charIR)):
    class_map = {c['Class']: c for c in charTab[i]}             # class_map is dict of columns (classes) in charTab
    charTab[i] = [class_map[id]["Value"] for id in classList]   # charTab sorted such that rows match classList

# Print character table to screen
#
print classList
for i in charTab:
    print i
print

# Deserialise wyckoff position data
#   
#
shift=[]
for s in wp.pop(0)[0].replace("[M","M").replace(')]',')').split(', '):
    if s=='[]':
        break
    shift.append(Matrix(sympify(s)))
if len(shift)==0:
    shift.append(Matrix(sympify("0,0,0")))
i=0                             # Iterator
pos, ptitle=[],[]               # pos contains the Wyckoff positions
                                # ptitle contains the names of the Wyckoff positions (Multiplicty+Letter)
for a in wp:
    ptitle.append(a[0]+a[1])
    pos.append([])
    for b in a[3].split(', '):
        c=b.replace('[M','M').replace(')]',')') # Removes left over braces
        pos[i].append(Matrix(sympify(c)))
    i+=1

# Calculate atomic character
#
i=0
achar=[]
subZero=[(x,0),(y,0),(z,0)]
for a in pos:
    achar.append([])
    for t in transforms:
        count=0
        for b in a:
            c=t[0]*b+t[1]
            if not (c in a):    # If outside of cell, place inside.
                d=c.subs(subZero)
                for j in range(len(d)):
                    c[j]=c[j]-1 if d[j]>=1 else c[j]
                    c[j]=c[j]+1 if d[j]<0 else c[j]
                if not (c in a):
                    for s in shift:
                        cShift=c-s
                        d=cShift.subs(subZero)
                        for j in range(len(d)):
                            cShift[j]=cShift[j]-1 if d[j]>=1 else cShift[j]
                            cShift[j]=cShift[j]+1 if d[j]<0 else cShift[j]
                        if (cShift in a):
                            c=cShift
                            break
            if c==b:
                count+=1
        achar[i].append(count)
    i+=1

# Calculate displacement character
#
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

a,ss=[],[]
comm="ss=solve_linear_system(system"
for i in charIR:
    a.append(symbols(str(i)))
    comm=comm+",a["+str(len(a)-1)+"]"
comm=comm+")"

for i in range(len(ptitle)):
    system=systemSeed.col_insert(len(charTab[i]),Matrix(char[i]))
    exec(comm)
    for j in a:
        ss[j]=ss[j].expand(complex=True)
    print ptitle[i], ss

#So, solve will accept a list of values, but solve_linear_system will not. Bummer.
# Is perUnitCell needed? It leads to fractional values... Work out 204 8c myself, I guess.