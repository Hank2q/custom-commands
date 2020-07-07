import pyautogui
from sys import argv
import datetime

ss_path = "C:/Users/HASSANIN/Pictures/screenshots"

ss = pyautogui.screenshot()
if len(argv) > 1:
    name = argv[1]
else:
    name = datetime.datetime.now().strftime("%d-%m-%Y %H.%M.%S")

ss.save(f'{ss_path}/{name}.png')
