import cv2
import glob
from PIL import Image, ImageDraw, ImageFont


def white(x1, x2, y1, y2, path):
    img = cv2.imread(path)
    cv2.rectangle(img,(x1,y1),(x2,y2),(255, 255, 255),-1)
    cv2.imwrite(path, img)
        
        
#white(500, 600, 200, 300, 'images\download.jpg')