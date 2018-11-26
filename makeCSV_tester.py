import csv
import numpy as np

test=({'title': '1', 'rot': np.array([[1,0,0],[0,1,0],[0,0,1]]), 'trans': np.array([[0],[0],[0]])}, \
        {'title': '2 (0,0,1/2) 1/4,0,z ', 'rot': np.array([[-1,0,0],[0,-1,0],[0,0,1]]), 'trans': np.array([[1/2.],[0],[1/2.]])})

with open('test.csv', 'wb') as csvfile:
    fieldnames=['title', 'rot', 'trans']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in test:
        writer.writerow(i)

with open('test.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['title'], row['rot'], row['trans'])
        aa=np.array(row['rot'].replace('\n', ','))
        bb=np.array(row['trans'].replace('\n', ','))
        print aa
        print bb
        print 



