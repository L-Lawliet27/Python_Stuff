import PySimpleGUI as sg
from guiComponents import setInitalProgress, buttonEventListener, initiateWindowElements
from addSeries import getSeries

# MAIN
# -------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    sg.theme("DarkBlue13")
    window, progBarValues, buttonMaxValues, buttonsBooks = initiateWindowElements()
    run = True
    setBar = True

    while run:
        try:
            event, values = window.read(timeout=1)
            if event == "__TIMEOUT__" and setBar:
                setInitalProgress(window, progBarValues)
                setBar = False
            if event == sg.WIN_CLOSED or event == 'Close':
                run = False
            if run:
                buttonEventListener(sg, event, buttonsBooks,
                                    progBarValues, buttonMaxValues, window)
                if event == "-READNEXT-":
                    sg.popup("TBT")
                elif event == "-INPUTBUTTON-":
                    url = values["-INPUT-"]
                    setBar=getSeries(url)
                    window["-INPUT-"].update("")
                    window.close()
                    window, progBarValues, buttonMaxValues, buttonsBooks = initiateWindowElements()

        except Exception as e:
            sg.popup_error(str(e))
    window.close()

# -------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
    