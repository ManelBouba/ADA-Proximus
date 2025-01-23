import csv

def csv_reader(path):
    """
    Reads a CSV file and returns its contents as a list of dictionaries.
    Args:
        path (str): The file path to the CSV file.
    Returns:
        list: A list of dictionaries where each dictionary represents a row in the CSV file.
    """
    result = []
    with open(path, 'r') as file:
        for row in csv.DictReader(file):
            result.append(row)

    return result
