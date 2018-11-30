# CSV_IO contains methods which write out and read in csv files.
#
import csv

# csvWrite
#       Takes data and writes it to a csv file.
#       Input:  filename (str) - Name of output file
#               fieldnames (List: str) - List of column names for data
#               data (List) - Data to be output 
def csvWrite(filename, fieldnames, data):
    with open(filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in data:
            writer.writerow(i)

# csvRead
#       Reads data from a csv file and returns it.
#       Input:  filename (str) - Name of input file
#               fieldnames (List: str) - List of column names for data
#       Output: data (List: str) - Data to be output 
def csvRead(filename, fieldnames):
        data=[]
        with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                        data.append(map(lambda x: row[x], fieldnames))
        return data
