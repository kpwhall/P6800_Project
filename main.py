from CSV_IO import csvRead
import numpy as np

SPACE=204
K=[0,0,0]
POS=[np.array([[0],[0],[0]]),np.array([[1./2],[1./2],[1./2]])]

print csvRead("./data/ge/ge"+str(SPACE)+".csv", ['ITA', 'rot', 'trans'])