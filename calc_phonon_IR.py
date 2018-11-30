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
#   Take each group element in the data and convert it to a 
#   form usable by this code.
#   Classes and one associated element are appended are collected by 
#   only considering the first part of the name. This method of getting classes 
#   doesn't work in all cases as there isn't a 1:1 correlation between element 
#   names and class names. It works for the cases tested, however.
#
transforms,classList=[],[]  # transforms Contains list of group elements as a list [Rotation, Transform, Name]    
                            # classList Contains (incorrect, see above) list of classes
for g in ge:
    if (not g[0].split()[0] in classList):
        classList.append(g[0].split()[0])                                       # Append class name
        transforms.append([Matrix(sympify(g[1])),Matrix(sympify(g[2])),g[0]])   # Append transforms in (rotation, translation) pair

# Deserialise character table data
#   Take each element of the character tables from data and 
#   convert to a form usable by this code.
#
charIR,charTab=[],[]    # charIR - list of IR names
                        # charTab - list of characters
i=0                     # Iterator
for t in ct:
    charIR.append(t[0]) # Append IR name
    charTab.append([])
    for l in t[1].replace('[','').replace(']','').split(','):
        a=l.replace('{','').replace('}','').replace("'","").split(':')      # Break up string.
        charTab[i].append({"Class": a[0].strip(), "Value": sympify(a[1])})  # Add values associated with each class.
    i+=1

# Sort charTab to match ordering in classList
#   Take the (incorrect) list of classes
#
for i in range(len(charIR)):
    class_map = {c['Class']: c for c in charTab[i]}             # class_map is dict of columns (classes) in charTab
    charTab[i] = [class_map[id]["Value"] for id in classList]   # charTab sorted such that rows match classList

# Print character table to screen
#   That's it.
print
print classList
for line in charTab:
    print line
print

# Deserialise wyckoff position data
#   Take the data read in from the wyckoff position file and 
#   transform it to a form we can use
#
shift=[]    # shift - list of shifts for each primitive unit cell
for s in wp.pop(0)[0].replace("[M","M").replace(')]',')').split(', '):  # String management + Separate into list of shifts
    if s=='[]':                                                         # If shift doesn't exist, add a 0 vector
        shift.append(Matrix(sympify("0,0,0")))
    shift.append(Matrix(sympify(s)))                                    # Append shifts
    
i=0                             # Iterator
pos, ptitle=[],[]               # pos - Wyckoff positions
                                # ptitle - Wyckoff positions names (Multiplicty+Letter)
for a in wp:
    ptitle.append(a[0]+a[1])    # Append Multiplicity+Letter as name
    pos.append([])
    for b in a[3].split(', '):                  # Collect Wyckoff positions
        c=b.replace('[M','M').replace(')]',')') # String management
        pos[i].append(Matrix(sympify(c)))
    i+=1

# Calculate atomic character
#   Atomic characters are calculated by determining how many of the positions
#   return to themselves after a transformation.
#
i=0                             # Iterator
achar=[]                        # achar - Atomic characters
subZero=[(x,0),(y,0),(z,0)]     # subZero - Define a substition setting x,y,z -> 0,0,0
for a in pos:
    achar.append([])
    for t in transforms:
        count=0
        for b in a:
            c=t[0]*b+t[1]               # Transform
            if not (c in a):            # If outside of cell, place inside.
                d=c.subs(subZero)       # Substitute symbols to zero
                for j in range(len(d)): # Attempt to bring into unit cell
                    c[j]=c[j]-1 if d[j]>=1 else c[j]
                    c[j]=c[j]+1 if d[j]<0 else c[j]
                if not (c in a):        # If still outside
                    for s in shift:     # Apply shifts
                        cShift=c-s
                        d=cShift.subs(subZero)
                        for j in range(len(d)): # Attempt to bring into unit cell
                            cShift[j]=cShift[j]-1 if d[j]>=1 else cShift[j]
                            cShift[j]=cShift[j]+1 if d[j]<0 else cShift[j]
                        if (cShift in a):       # If shift works, break.
                            c=cShift
                            break
            if c==b:                        # If position is the same, increment count
                count+=1
        achar[i].append(count)              # Append count.
    i+=1

# Calculate displacement character
#   Use symbolic math to determine the trace of all of the transforms
#   when acting on a generic (x,y,z) vector.
#
vec=Matrix(sympify("[[x],[y],[z]]"))    # Vector to be transformed
dchar=[]                                # List to hold displacement characters
i=0                                     # Iterator
for t in transforms:
    count=0
    tvec=t[0]*vec+t[1]                  # Apply transform
    for i in range(3):                  # Calculate trace
        count += 1 if tvec[i]==vec[i] else 0    # If same, increment.
        count -= 1 if tvec[i]==-vec[i] else 0   # If negative, decrement
    dchar.append(count)

# Combine total characters
#   Simply multiply the wyckoff position atomic character by the displacement
#   character. The three characters are then ouput for each position.
#
char=[]     # Char holds the total character
for i in range(len(ptitle)):
    char.append([])
    for j in range(len(achar[i])):
        char[i].append(achar[i][j]*dchar[j])
    print ptitle[i]
    print "Atomic character:       ", achar[i]
    print "Displacement character: ", dchar
    print "Total character:        ", char[i]
    print

# Solve system of linear equations
#   By considering all of the characters of each class for an IR
#   and the calculated character as a system of linear equations
#   we can simply solve that system. (IRs)*(Multiplicity of IRs)=(Calculated characters)
#
systemSeed=Matrix() # Creates the left hand side of linear equations
for r in charTab:
    systemSeed=systemSeed.col_insert(len(systemSeed)/len(r),Matrix(r))   # Need to ensure the columns are lined up correctly.

a,ss=[],[]  # a - list of IRs as symbols for symbolic math
            # ss - system solution (will hold solutions)

#############################################################################
# comm is a string which defines our function                               #
# This is done because the SymPy method solve_linear_system will not        #
# accept a list of symbols as an argument. It needs that all symbols        #
# are explicitly listed. By doing this, I am able to store them as a list   #
# and run the string as if it were code by using the exec command later.    #
# This allows for generalised code, although it isn't pretty.                #
#############################################################################
comm="ss=solve_linear_system(system"
for i in charIR:
    a.append(symbols(str(i)))
    comm=comm+",a["+str(len(a)-1)+"]"
comm=comm+")"

# Solve each equation and print result to screen
#   And print out a little info on dimensionality and the space group
#
if shift[0] != Matrix(sympify("0,0,0")):        # If the space group isn't type P
    print "In space group "+str(SPACE)+" there are "+str(len(shift)+1)+" primitive cells per unit cell."
else: 
    print "In space group "+str(SPACE)+" there is 1 primitive cells per unit cell."
print "The dimensionality of these Wyckoff positions phonon modes should be (Multiplicity)*(Dimensions)/(# Primitive Cells).\n"
for i in range(len(ptitle)):
    system=systemSeed.col_insert(len(charTab[i]),Matrix(char[i]))   # append the calculated char to the system
    exec(comm)
    for j in a:
        ss[j]=ss[j].expand(complex=True)
    print ptitle[i], ss