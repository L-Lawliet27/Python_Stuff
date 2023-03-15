import json
from datetime import date


# Listener for ReadButton and dateRead events
# -------------------------------------------------------------------------------------------------------------------------------------------------
def readListener(event, values, window, totalCompletionValue):
    i = 1
    found = False
    while i <= totalCompletionValue and not found:
        readDateKey = f"-DREAD{i}-"
        readCheckBoxKey = f"-READ{i}-"

        if event == readCheckBoxKey:
            if values[readCheckBoxKey] and values[readDateKey] in (None, "", []):
                today = date.today().strftime("%y-%m-%d")
                window[readDateKey].update(today)
                values[readDateKey]=today
            elif not values[readCheckBoxKey] and values[readDateKey] not in (None, "", []):
                window[readDateKey].update("")
                values[readDateKey]=""
            found = True

        elif event == readDateKey:
            if not values[readCheckBoxKey] and values[readDateKey] not in (None, "", []):
                window[readCheckBoxKey].update(True)
                values[readCheckBoxKey]=True
            elif values[readCheckBoxKey] and values[readDateKey] in (None, "", []):
                window[readCheckBoxKey].update(False)
                values[readCheckBoxKey]=False
            found = True
        i+=1
# -------------------------------------------------------------------------------------------------------------------------------------------------


# Update completion
# -------------------------------------------------------------------------------------------------------------------------------------------------
def updatePercent(values, seriesTitle, currentCompletionValue, totalCompletionValue):
    booksReadCounter = 0
    for i in range(1, totalCompletionValue+1):
        if values[f"-READ{i}-"]:
            booksReadCounter += 1

    if booksReadCounter == 0 or booksReadCounter == currentCompletionValue:
        return "", 0

    elif currentCompletionValue < totalCompletionValue:
        currentCompletionValue = booksReadCounter
        newPercent = f"({currentCompletionValue/totalCompletionValue:.0%})"
        updatedName = f"{seriesTitle} {newPercent}"
        return updatedName, currentCompletionValue

# -------------------------------------------------------------------------------------------------------------------------------------------------

# Update individual entries
# -------------------------------------------------------------------------------------------------------------------------------------------------
def updateEntries(entries, values):
    for i, bookName in enumerate(entries, 1):
        entries[bookName]["boughtOn"] = values[f"-BOUGHT{i}-"]
        entries[bookName]["readOn"] = values[f"-DREAD{i}-"]
        entries[bookName]["read"] = values[f"-READ{i}-"]
# -------------------------------------------------------------------------------------------------------------------------------------------------


# Save Updated Values to the JSON file
# -------------------------------------------------------------------------------------------------------------------------------------------------
def saveValuesToJson(seriesTitle, series, updatedCompletionValue, values):
    with open('bookData.json', 'r') as readFile:
        seriesList = json.load(readFile)
    if updatedCompletionValue != 0:
        series["completion"] = updatedCompletionValue 
    updateEntries(series["entries"], values)
    seriesList[seriesTitle] = series

    with open('bookData.json', 'w') as writeFile:
        json.dump(seriesList, writeFile, indent=4)
# -------------------------------------------------------------------------------------------------------------------------------------------------



#The one that involves creating each individual book's componenet for a series 

# INIT Series ENTRIES
# -------------------------------------------------------------------------------------------------------------------------------------------------# -------------------------------------------------------------------------------------------------------------------------------------------------
def initSeriesEntries(sg, seriesEntries):
    bookFont = ("Merriweather", 14)
    bookEntries = []
    # seriesEntries is the dictionary of seriesList[series], series being the name of the series, as to access its dict
    for i, book in enumerate(seriesEntries, 1):
        bookEntry = sg.Text(book, font=bookFont)
        boughtOn = seriesEntries[book]["boughtOn"]
        readOn = seriesEntries[book]["readOn"]
        read = seriesEntries[book]["read"]

        bookEntries.append([bookEntry])
        bookEntries.append([sg.CalendarButton("Date Bought", close_when_date_chosen=True, target=f"-BOUGHT{i}-", format="%y-%m-%d"),
                            sg.Input(key=f"-BOUGHT{i}-", size=(7, 1), change_submits=True, default_text=boughtOn),
                            sg.CalendarButton("Date Read", close_when_date_chosen=True,
                                              target=f"-DREAD{i}-", format="%y-%m-%d"), sg.Input(key=f"-DREAD{i}-", size=(7, 1), change_submits=True, default_text=readOn),
                            sg.Checkbox("", default=read, key=f"-READ{i}-", change_submits=True)
                            ])
    return bookEntries
# -------------------------------------------------------------------------------------------------------------------------------------------------

#The Window for the Books of a Series

# BOOK WINDOW
# -------------------------------------------------------------------------------------------------------------------------------------------------
def booksWindow(sg, progBarValues, prog, buttonMaxValues, mainWindow, key, buttonName):

    buttonRow = [sg.Button('Return')]

    index = buttonName.index('(')

    seriesTitle = buttonName[0:index-1]

    with open('bookData.json', 'r') as readFile:
        seriesList = json.load(readFile)
        series = seriesList[seriesTitle]

    seriesEntries = initSeriesEntries(sg, seriesEntries=series["entries"])
    seriesAuthor = series['author']

    font = ("Arial", 25)
    authorFont = ("Arial", 15)
    title = sg.Text(seriesTitle, justification="center",
                    size=(50, 1), font=font, key="-TITLE-")
    authors = sg.Text(seriesAuthor, justification="center",
                      size=(50, 1), font=authorFont, key="-AUTHOR-")

    mainLayout = [[title], [authors], [sg.Column(
        seriesEntries, scrollable=True, size=(300, 304)), sg.Sizer(280, 308)], [buttonRow]]

    window = sg.Window(seriesTitle, layout=mainLayout, size=(350, 450))

    updatedName=""
    updatedCompletionValue=0

    run = True
    while run:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Return':
            run = False

        readListener(event, values, window, totalCompletionValue=buttonMaxValues[prog])
        
        if run:
            updatedName, updatedCompletionValue = updatePercent(
                values, seriesTitle, progBarValues[prog], buttonMaxValues[prog])

            if updatedName != "" and updatedCompletionValue != 0:
                mainWindow[key].update(text=updatedName)
                mainWindow[prog].UpdateBar(updatedCompletionValue)
                progBarValues.update({prog: updatedCompletionValue})
        else:
            saveValuesToJson(seriesTitle, series, updatedCompletionValue, values)
    window.close()
# -------------------------------------------------------------------------------------------------------------------------------------------------
