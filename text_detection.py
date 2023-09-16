import io
import os
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from google.cloud import vision
from google.cloud import translate


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'shentai_file.json'

client = vision.ImageAnnotatorClient()

image_path = 'images\download.jpg'

Text_Detection = namedtuple('Text_Detection', ('description', 'bounding_poly'))


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
    
    return returnString
    
texts = text_detection(image_path)
print(texts)

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
            "target_language_code": "en",
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print(f"Translated text: {translation.translated_text}")

    return response

textT = translate_text(texts)
#rint(textT)