import pyautogui as pg
import time

print("text to u auto")
time.sleep(5)

for i in range(10):
    pg.write("I miss you")
    time.sleep(0.5)
    pg.press("Enter")