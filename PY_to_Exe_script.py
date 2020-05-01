import cx_Freeze
import sys
import cv2
import tkinter
import PIL
import os

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("Center_Face_detection_Gui.py", base=base)]

cx_Freeze.setup(
    name = "SeaofBTC-Client",
    options = {"build_exe": {"packages":["tkinter","cv2","os","PIL"], "include_files":["Haarcascade"]}},
    version = "0.01",
    description = "This is center face detection app",
    executables = executables
    )