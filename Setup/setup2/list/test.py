import csv

f = open("EMR.txt",'rb')
g = csv.reader(f,delimiter='\t')
data = []
for row in g:
    data.append(row[0])

f.close()
del data[0]
del data[0]

print data
