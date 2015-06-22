import csv

def transform(filename):
    return "../" + filename

def read_csv(filename):
    data = []
    import os
    print os.getcwd()
    f = open(filename, 'rb')
    reader = csv.reader(f)
    for i,row in enumerate(reader):
        if i == 0 : continue  # Header
        data.append([i-1]+row)
    return data


