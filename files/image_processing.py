import cv2

def white_out(x1, x2, y1, y2, path):
    img = cv2.imread(path)
    cv2.rectangle(img,(x1,y1),(x2,y2),(255, 255, 255),-1)
    cv2.imwrite(path, img)
        
        
#white(500, 600, 200, 300, 'images\download.jpg')

def sharpie_marker(x ,y, path, text):
    # Reading an image in default mode
    img = cv2.imread(path)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    org = (x, y)
    fontScale = 1
    color = (0, 0, 0)
    thickness = 2
    img = cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False) # Change to true to change where it renders from
    # Displaying the image
    cv2.imwrite(path, img)