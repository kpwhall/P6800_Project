import csv

def csvWrite(filename, fieldnames, data):
    with open(filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in data:
            writer.writerow(i)


def csvRead(filename, fieldnames):
        data=[]
        with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                        data.append(map(lambda x: row[x], fieldnames))
        return data
                        
