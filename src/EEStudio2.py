#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#! /usr/bin/env python3

"""
Created on 10.11.2020 22:17 CET

@author: zocker_160
"""

import sys

#import PySimpleGUI as gui
import PySimpleGUIQt as gui
from PySimpleGUIQt.PySimpleGUIQt import Button

# Empire Earth tools
from lib.SSAtool.src import SSAtool

#print( gui.ListOfLookAndFeelValues() )
#print(gui.LOOK_AND_FEEL_TABLE.get("SystemDefault"))

gui.LOOK_AND_FEEL_TABLE["custom"] = {
    'BACKGROUND': 'grey',
    'TEXT': 'black',
    'INPUT': '#DDE0DE',
    'SCROLL': '#E3E3E3',
    'TEXT_INPUT': 'black',
    'BUTTON': ('black', 'darkgrey'),
    'PROGRESS': gui.DEFAULT_PROGRESS_BAR_COLOR,
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0
}

BUTTON_SIZE = (15, 1)
#gui.theme("DarkTeal2")
#gui.theme("Dark2")
gui.theme("custom")

### window layouts
main_layout = [
    [
        gui.Button("Main", size=BUTTON_SIZE),
        gui.Button("Archives (SSA)", size=BUTTON_SIZE, key="SSA"),
        gui.Button("Textures (SST)", size=BUTTON_SIZE, key="SST"),
        gui.Button("3D Models (CEM)", size=BUTTON_SIZE, key="CEM"),
        gui.Button("About", size=(7, 1)),
        gui.Button("Exit", size=(7, 1)),
    ],
    #[gui.Output(visible=True, key="OO")],
]

ssa_layout = [
    [gui.Text("Select SSA file", text_color="white")],
    [gui.Text("Inputfile       "), gui.Input(key="IN"), gui.FileBrowse("Browse", file_types=(("SSA archives", "*.ssa"),)) ],
    [gui.Text("Outputfolder"), gui.Input(key="OUT"), gui.FolderBrowse("Browse")],
    [gui.Checkbox("decompress files", default=True, key="decompress")],
    [gui.Button("Convert", size=BUTTON_SIZE), gui.Button("Show filelist"), gui.Button("Cancel", size=BUTTON_SIZE, key="ssa_exit")]
]

###

main_window = gui.Window(
    "Empire Earth Studio II - Empire Earth Reborn",
    main_layout,
)

ssa_window = gui.Window(
    "SSA Extractor",
    ssa_layout,
)

###

def ssatool():
    ssa_window.un_hide()
    while True:
        event, value = ssa_window.read()

        # events SSA
        if event == "ssa_exit":
            print("WINDOW CLOSE!")
            #main_window["OO"].update(visible=False)
            
            ssa_window.hide()
            break
        if event == "Convert":
            #main_window["OO"].update(visible=True)
            print(value)

            SSAtool.main(inputfile=value["IN"], outputfolder=value["OUT"], decompress=value["decompress"])
            #ssafake.main(infile=value["IN"], outfile=value["OUT"])

            ssa_window.hide()
            break


if __name__ == "__main__":
    
    while True:
        event, value = main_window.read()
        print("event", event)
        print("values", value)

        # events main window
        if event == "Exit" or gui.WINDOW_CLOSED or not event:
            break
        if event == "SSA":
            ssatool()


    main_window.close()
