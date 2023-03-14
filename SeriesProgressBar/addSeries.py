import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import validators
# Everything Involving Adding a New Series

# This function takes the url from amazon and returns the entire info of the series as a list
# -------------------------------------------------------------------------------------------------------------------------------------------------
def getSeries(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    if not validators.url(url):
        raise Exception("Invalid URL")

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    seriesName = soup.find(
        'span', {'id': "collection-title"}).text.strip().title()

    author = ""
    currentLenght = 0
    group = soup.find_all('div', {'id': 'series-childAsin-batch_1'})
    groupBooks = group[0].findChildren('div', recursive=False)
    series = {"completion": 0, "author": "", "entries": {}}
    for book in groupBooks:

        bookName = book.find(
            'a', {'class': 'a-size-medium a-link-normal itemBookTitle'}).text.strip().title()

        if ':' in bookName:
            bookName = book.find(
                'a', {'class': 'a-size-medium a-link-normal itemBookTitle'}).text.strip().split(':')[0].rstrip()
        elif ' (' in bookName:
            bookName = book.find(
                'a', {'class': 'a-size-medium a-link-normal itemBookTitle'}).text.strip().split(' (')[0].rstrip()

        authorName = book.find_all(
            'a', {'class': 'a-link-normal series-childAsin-item-details-contributor'})

        if author == "" or currentLenght < len(authorName):
            first_author = authorName[0].text.strip()[:-26]
            second_author = authorName[1].text.strip(
            )[:-8] if len(authorName) == 2 else ""
            author = f"{first_author}, {second_author}" if second_author else first_author
            series['author'] = author
            currentLenght = len(authorName)

        series["entries"][bookName] = {
            'boughtOn': 0, 'readOn': 0, 'read': False}

    driver.close()
    return saveSeries(seriesName, series)
# -------------------------------------------------------------------------------------------------------------------------------------------------


# This function adds new entries to a series if the author publishes a new book
# -------------------------------------------------------------------------------------------------------------------------------------------------
def addNewEntries(seriesListEntries, seriesEntries):
    for bookName, values in seriesEntries.items():
        seriesListEntries.setdefault(bookName, values)
    return True
# -------------------------------------------------------------------------------------------------------------------------------------------------


# This function gets the list from getSeries() and saves it to the JSON file
# -------------------------------------------------------------------------------------------------------------------------------------------------


def saveSeries(seriesName, series):
    newEntriesAdded = False
    with open('bookDataTest.json', 'r') as readFile:
        seriesList = json.load(readFile)
    if seriesName in seriesList.keys(): 
        if len(series["entries"]) == len(seriesList[seriesName]["entries"]):
            raise Exception("Series is already in app\n")
        else:
           newEntriesAdded=addNewEntries(seriesList[seriesName]["entries"], series["entries"])
    else:
        seriesList[seriesName] = series
    with open('bookDataTest.json', 'w') as writeFile:
        json.dump(seriesList, writeFile, indent=4)
    return newEntriesAdded
# -------------------------------------------------------------------------------------------------------------------------------------------------