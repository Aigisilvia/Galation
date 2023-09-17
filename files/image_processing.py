import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw 

def process_image(x1, x2, y1, y2, path, text):
    img = cv2.imread(path)
    cv2.rectangle(img,(x1,y1),(x2,y2),(255, 255, 255),-1)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    org = (x, y) #Origin of character
    fontScale = .75
    color = (0, 0, 0)
    thickness = 1
    img = cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False) # Change to true to change where it renders from
    cv2.imwrite(path, img)
    
process_image(500, 750, 200, 300, 'images\download.jpg', 'She farded on my dick')

