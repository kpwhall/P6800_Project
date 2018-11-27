import csv
import numpy as np

test=[{'ITA': '1', 'rot': np.array([[1,0,0],[0,1,0],[0,0,1]]), 'trans': np.array([[0],[0],[0]])}, \
        {'ITA': '2 (0,0,1/2) 1/4,0,z ', 'rot': np.array([[-1,0,0],[0,-1,0],[0,0,1]]), 'trans': np.array([[1/2.],[0],[1/2.]])}]

def csvWrite(filename, fieldnames, data):
    with open(filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in data:
            writer.writerow(i)


def csvRead(filename, fieldnames):
        ge=[]
        with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                        a=np.fromstring(row['rot'].replace("\n","").replace("[","").replace("]","").replace(",",""), sep=" ").reshape(3,3)
                        b=np.fromstring(row['trans'].replace("\n","").replace("[","").replace("]","").replace(",",""), sep=" ")
                        ge.append((a,b))
        return ge
                        
