#web_url_grabber

from import_list import *
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from google.cloud import vision
from google.cloud import translate_v2 as translate
from google.cloud import storage
from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver



#Chrome URL grabber, starts the driver and gets page source
driver = webdriver.Chrome()
driver.get(driver.current_url)
results = []
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

#gets url attributes
def gets_url(classes, location, source):
    results = []
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name not in results:
            results.append(name.get(source))
            driver.quit()  #stops grabbing the page, it has grabbed all information needed and attributes
    return results

#puts image and attributes into a png
def convert_url():
    if __name__ == "__main__":
        returned_results = gets_url("s-item__image-wrapper image-treatment", "img", "src")
    for b in returned_results:
        image_content = requests.get(b).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")
        file_path = Path("C:\Users\Grayson\Pictures", hashlib.sha1(image_content).hexdigest()[:10] + ".png") #Change to your file path for now (we can have a user defined path or a general one later)
        image.save(file_path, "PNG", quality=80)
        
        #returns the file path of the image in order to upload it to the bucket
        return file_path
        
        #pip install --upgrade google-cloud-storage. 
def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""
     
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json('shentai_file.json')

    #print(buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    
    #returns a public url
    return blob.public_url