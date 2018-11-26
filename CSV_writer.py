import csv
import numpy as np

test=({'ITA': '1', 'rot': np.array([[1,0,0],[0,1,0],[0,0,1]]), 'trans': np.array([[0],[0],[0]])}, \
        {'ITA': '2 (0,0,1/2) 1/4,0,z ', 'rot': np.array([[-1,0,0],[0,-1,0],[0,0,1]]), 'trans': np.array([[1/2.],[0],[1/2.]])})

with open('test.csv', 'wb') as csvfile:
    fieldnames=['ITA', 'rot', 'trans']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in test:
        writer.writerow(i)

with open('test.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['ITA'], row['rot'], row['trans'])
        print row['rot'].replace("\n","").replace("[","").replace("]","").replace(",","")
        print row['trans'].replace("\n","").replace("[","").replace("]","").replace(",","")
        print
        aa=np.fromstring(row['rot'].replace("\n","").replace("[","").replace("]","").replace(",",""), sep=" ").reshape(3,3)
        bb=np.fromstring(row['trans'].replace("\n","").replace("[","").replace("]","").replace(",",""), sep=" ")
        print aa
        print bb
        print aa*bb
        print



