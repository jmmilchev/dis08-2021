import bs4, csv, json, re
import pandas as pd
from requests_cache import CachedSession

# Step 1: pick a wikipedia page
## Setting global variables
### the base url for the wikipedia page
wikipediaBaseUrl = 'https://de.wikipedia.org'
### the url of the page with the table containing names and links to other Wikipedia pages
baseTableUrl = wikipediaBaseUrl + '/wiki/Liste_der_gr%C3%B6%C3%9Ften_Unternehmen_der_Welt'
### the html selector for the table
baseTableSelector = '.mw-parser-output > .wikitable:first-of-type > tbody > tr:nth-of-type(1n+2)'
### a string for identifying the table containing the details
detailTableMatch = 'Rechtsform'
### list of values to fetch from the table
datailValues = ['Rechtsform', 'Mitarbeiterzahl', 'Umsatz', 'Sitz', 'Gründung']

## Prepare output files
### all files should be emptied at opening and created if not existing
### the csv file needs to be opened for writing and reading
csvFile = open('exercise3_result.csv', 'w+')
### pass the csv file to the csv writer
csvWriter = csv.writer(csvFile)
### insert the column names
csvWriter.writerow(['Name', 'URL'])
### the json file needs to be opened just for writing, but with UTF-8 encoding
jsonFile = open('exercise3_result.json', 'w', encoding='utf-8')

## Prepare session
### as suggested in the hints, use requests_cache to cache the requests
### the data should be cached for one day
session = CachedSession(backend='sqlite', expire_after=86400)
### get the content of the base table
baseTableSession = session.get(baseTableUrl)

## Parse base table
### create a beautiful soup object from the base table
baseTableHtml = bs4.BeautifulSoup(baseTableSession.text, features='html.parser')
### get the table containing the names and links
baseTable = baseTableHtml.select(baseTableSelector)

# Step 2: get all names and links from the base table
## Iterate over base table
print('Iterating over base table...')
for row in baseTable:
    ### get the first link in the row, as it contains the needed data
    element = row.select_one('a:first-of-type')
    ### prepare the csv row
    csvRow = [
        ### the name of the row
        element.text,
        ### the url to the detailled Wikipedia page
        wikipediaBaseUrl + element.attrs['href'],
    ]
    ### write the row to the csv file
    csvWriter.writerow(csvRow)

# Step 3: get all details from the detailled Wikipedia pages
## Prepare to fetch data
### jump to the beginning of the file
csvFile.seek(0, 0)
### pass the csv file to the csv reader
csvReader = csv.DictReader(csvFile)
### create an empty dictionary for the json file
data = {}

## Iterate over csv rows
print('Iterating over csv rows...')
for row in csvReader:
    print(row['Name'] + ", " + row['URL'])

    ### prepare the json row
    data[row['Name']] = {}
    ### get the content of the detailled table
    detailTableSession = session.get(row['URL'])
    ### create a beautiful soup object from the first matching table
    df = pd.read_html(detailTableSession.text, match=detailTableMatch, attrs={'class': 'toccolours'}, index_col=0, header=0, skiprows=0, thousands='.', decimal=',')[0]
    ### give the column a meaningful name
    df.columns = ['Value']
    ### transpose index and columns for easier access
    table = df.transpose()

    ### iterate over the values to fetch
    for value in datailValues:
        ### get the value from the table and make sure the script doesn't crash if the value is missing
        rawData = table.get(value)[0] if table.get(value) is not None else 'N/A'
        ### clean the data
        data[row['Name']][value] = re.sub(r'\(.+?\)', '', re.sub(r'\[.+?\]', '', rawData)).strip()

# Step 4: write the data to the json file
## Write json file
print('Writing json file...')
json.dump(data, jsonFile, ensure_ascii=False, indent=4)

## Close files
csvFile.close()
jsonFile.close()

print('Done.')
