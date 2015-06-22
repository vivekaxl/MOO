import csv

def transform(filename):
    return "../" + filename

def read_csv(filename, class_name):
    data = []
    import os
    print os.getcwd()
    f = open(filename, 'rb')
    reader = csv.reader(f)
    for i,row in enumerate(reader):
        if i == 0 : continue  # Header
        data.append(class_name(row))
    return data


