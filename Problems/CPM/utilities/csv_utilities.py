import csv

def transform(filename):
    return "../" + filename

def read_csv(filename, header=False):
    data = []
    print filename
    f = open(filename, 'rb')
    reader = csv.reader(f)
    for i,row in enumerate(reader):
        if i == 0 and header is False: continue  # Header
        elif i ==0 and header is True:
            H = row
            continue
        data.append([i-1]+[1 if x =="Y" else 0 for x in row[:-1]] + [int(row[-1])])
    f.close()
    if header is True: return H, data
    return data

