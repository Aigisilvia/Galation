from PIL import Image, ImageDraw, ImageFont


"""def white_out(x1, x2, y1, y2, path, text):
    img = cv2.imread(path)
    cv2.rectangle(img,(x1,y1),(x2,y2),(255, 255, 255),-1)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    org = (x, y) #Origin of character
    fontScale = .75
    color = (0, 0, 0)
    thickness = 1
    img = cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False) # Change to true to change where it renders from
    cv2.imwrite(path, img)
        
        


def sharpie_marker(x ,y, path, text):
    img = cv2.imread(path)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    org = (x, y) #Origin of character
    fontScale = .75
    color = (0, 0, 0)
    thickness = 1
    img = cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False) # Change to true to change where it renders from
    cv2.imwrite(path, img)
    
    
white_out(500, 750, 200, 300, 'images\download.jpg', 'She farded on my dick')
sharpie_marker(510,220,'images\download.jpg', 'She farded on my dick')
    """


def process_image(top_left, bottom_right, text, path):
    image = Image.open(path)
    draw = ImageDraw.Draw(image)
    text_color = (0)
    background_color = (255)
    font = ImageFont.load_default()

    background_width = abs(bottom_right[0] - top_left[0]) + 20 
    background_height = abs(bottom_right[1] - top_left[1]) + 20 

    background_x = min(top_left[0], bottom_right[0]) - 10  
    background_y = min(top_left[1], bottom_right[1]) - 10 

    draw.rectangle([background_x, background_y, background_x + background_width, background_y + background_height], fill=background_color)

    text_x = background_x + 10  
    text_y = background_y + 10  

    draw.text((text_x, text_y), text, fill=text_color, font=font)

    image.save(path)



process_image((100,100),(400,250), 'She farded on my dick', 'images\download.jpg')