import io
import os
import sys
import numpy
import re
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from google.cloud import vision
from google.cloud import translate

numpy.set_printoptions(threshold=sys.maxsize)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'shentai_file.json'

client = vision.ImageAnnotatorClient()

image_path = 'images\ONE-PIECE-618x472.png'

Text_Detection = namedtuple('Text_Detection', ('description', 'bounding_poly'))

parX = []
parY = []
vertices_list = []

def prepare_image_local(image_path):
    try:
        # Loads the image into memory
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        return image
    except Exception as e:
        print(e)
        return
    

    
def text_detection(self):
    with open(self, "rb") as image_file:
        content = image_file.read()
        
    image = vision.Image(content=content)
    
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")
    returnString = ''
    
    for text in texts:
        print(f'\n"{text.description}"')

        vertices = [
            f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        ]

        print("bounds: {}".format(",".join(vertices)))
        returnString +=  text.description
        vertices_list.append(vertices)
    
    return returnString
    
texts = text_detection(image_path)
print(texts)

vList = []

for layer in vertices_list:
    for row in layer:
        pair = []
        for element in row:
            if element.isdigit() or (element[0] == '-' and element[1:].isdigit()):
                pair.append(int(element))
            else:
                if pair:
                    vList.append(pair)
                    pair = []
        if pair:
            vList.append(pair)

vListC = []
#print(vList)
for pair in vList:
    combined_integer = int("".join(map(str, pair)))
    vListC.append(combined_integer)
#print(vListC)

"""
sizeResultx = []
prev_entry = None

for i in range(len(vListC)):
    current_entry = vListC[i]
    
    if i % 8 == 0 or i == 0:
        if prev_entry is not None and current_entry - prev_entry > 100:
            sizeResultx.append(prev_entry)
            sizeResultx.append(current_entry)
            break
        prev_entry = current_entry

print(sizeResultx)

sizeResulty = []
prev_entry = None

for i in range(len(vListC)):
    current_entry = vListC[i]
    
    if i % 8 == 0 or i == 0:
        if prev_entry is not None and current_entry - prev_entry > 100:
            sizeResultx.append(prev_entry)
            sizeResultx.append(current_entry)
            break
        prev_entry = current_entry

print(sizeResultx)
"""

textTrans = ''

def translate_text(
    text: str = texts, project_id: str = "shell-trandslation-2023"

 ) -> translate.TranslationServiceClient:
    """Translating Text."""

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "",
            "target_language_code": "en-US",
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print(f"Translated text: {translation.translated_text}")

    return response

textT = translate_text(texts)
print("\n")

print(textT)