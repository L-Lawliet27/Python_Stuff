import PySimpleGUI as sg
import json
from seriesEntriesWindow import booksWindow

# INIT URL GUIS
# -------------------------------------------------------------------------------------------------------------------------------------------------
def initAddingURLGUI():
    titleURL = sg.Text("Add Series via URL", size=(50, 1), font=("Arial", 10))
    inputURL = sg.Input(key="-INPUT-", size=(300, 40))
    inputButton = sg.Button("Enter", key="-INPUTBUTTON-", size=(5, 1))
    return [[titleURL], [inputURL], [inputButton]]
# -------------------------------------------------------------------------------------------------------------------------------------------------


# Set the Initial Value of the Progress Bars
# -------------------------------------------------------------------------------------------------------------------------------------------------
def setInitalProgress(window, progBarValues):
    for i in range(1,(len(progBarValues)+1)):
        progKey = f"-PROG{i}-"
        window[progKey].update(progBarValues[progKey])
# -------------------------------------------------------------------------------------------------------------------------------------------------


# INIT PROGRESS BARS
# -------------------------------------------------------------------------------------------------------------------------------------------------
def initSeriesComponents():
    with open('bookData.json', 'r') as readFile:
        seriesList = json.load(readFile)
    progBarValues = {}
    buttonMaxValues = {}
    buttonsBooks = []
    for i, series in enumerate(seriesList, 1):
        buttonMax = len(seriesList[series]['entries'])
        completionNum = seriesList[series]['completion']
        progKey = f"-PROG{i}-"
        progBar = sg.ProgressBar(buttonMax, orientation='h', size=(
            24.90, 20), key=progKey, bar_color=("Orange", "LightGrey"))
        progBarValues[progKey] = completionNum
        buttonMaxValues[progKey] = buttonMax
        seriesProgress = f"{series} ({completionNum/buttonMax:.0%})"
        buttonKey = f"-BUTTON{i}-"
        button = sg.Button(seriesProgress, key=buttonKey, size=(32, 1.25))
        buttonsBooks.extend([[button], [progBar]])

    return progBarValues, buttonMaxValues, buttonsBooks
# -------------------------------------------------------------------------------------------------------------------------------------------------


def initiateWindowElements():
    progBarValues, buttonMaxValues, buttonsBooks = initSeriesComponents()
    readNext = None  # TODO
    addSeries = initAddingURLGUI()

    layout1 = [[sg.Column(layout=buttonsBooks, scrollable=True,
                          size=(None, 304)), sg.Sizer(280, 308)]]
    layout2 = [[]]
    layout3 = [[sg.Column(addSeries, size=(None, 304)), sg.Sizer(280, 308)]]

    tab1 = sg.Tab('Series Progress', layout=layout1, title_color='Black',
                  border_width=80, element_justification='center', key="-TAB1-")
    tab2 = sg.Tab('Read Next', layout=layout2, title_color='Black',
                  border_width=80, element_justification='center', key="-TAB2-")
    tab3 = sg.Tab('Add Series', layout=layout3, title_color='Black',
                  border_width=80, element_justification='center', key="-TAB3-")

    tabs = [[tab1, tab2, tab3]]

    tabgrp = [[sg.TabGroup(
        layout=tabs, tab_location='centertop', border_width=5, key="-TABGROUP-")]]

    buttonRow = [sg.Button('Close')]

    mainLayout = [[tabgrp], [buttonRow]]

    window = sg.Window(title="TBR Progress",
                       layout=mainLayout, size=(305, 420))
    return window, progBarValues, buttonMaxValues, buttonsBooks



# Listens if user presses button of progress bars
# -------------------------------------------------------------------------------------------------------------------------------------------------
def buttonEventListener(sg, event, buttonsBooks, progBarValues, buttonMaxValues, window):
    for i in range(1, (len(buttonsBooks)+1)):
        key = f"-BUTTON{str(i)}-"
        if event == key:
            prog = f"-PROG{str(i)}-"
            booksWindow(sg, progBarValues, prog, buttonMaxValues,
                        window, key, buttonName=window[event].get_text())
# -------------------------------------------------------------------------------------------------------------------------------------------------
