import csv
from src.data.company_data import exchange_companies_data
from src.util.common_classes.filename_holder import FileNames


def readCsvFile():
    data = {}

    #with open(FileNames.dataFileName, newline='',encoding='utf-8',errors='ignore') as csvfile:
     #   reader = csv.DictReader(csvfile)

    with open(FileNames.dataFileName, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader((line.replace('\x00', '').replace('��','')for line in f))

        for row in reader:
            url = row['url'].strip()
            url = url.replace("https://www.","").replace("https://www","").replace('https://','')
            if url.endswith('/'):
                url = url[0:len(url)-1]
            data[url] = row
            # data.append(row)
    return data

def convert_to_number(value:str):
    try:
        return int(value)
    except Exception as err:
        return None

def mergeFiles():
    data = readCsvFile()
    list = []

    for company in exchange_companies_data:
        url = company['url']
        if url in data:


            newdata = data[url]
            merged_data = {**company, **newdata}
            merged_data['url'] = url

            if 'number_of_branches' in merged_data:
               number_of_branches = convert_to_number(merged_data['number_of_branches'])
               if (number_of_branches is not None):
                   merged_data['number_of_branches'] = number_of_branches

            list.append(merged_data)
        else:
            print(url)
    m = 5

mergeFiles()
