import csv

def transform(filename):
    return "../" + filename

def read_csv(filename):
    data = []
    f = open(filename, 'rb')
    reader = csv.reader(f)
    for i,row in enumerate(reader):
        if i == 0 : continue  # Header
        data.append([i-1]+[1 if x =="Y" else 0 for x in row[:-1]] + [row[-1]])
    return data


