import csv

def csv_reader(path):
    result = []
    with open(path, 'r') as file:
        for row in csv.DictReader(file):
            result.append(row)

    return result
