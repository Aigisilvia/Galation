import io
import os
import base64
import json

from cloudevents.http import CloudEvent

import functions_framework

from google.cloud import vision
from google.cloud import pubsub_v1
from google.cloud import translate_v2 as translate
from google.cloud import storage

vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
publisher = pubsub_v1.PublisherClient()
storage_client = storage.Client()

project_id = os.environ.get("shell-trandslation-2023")


@functions_framework.cloud_event
def process_image(cloud_event: CloudEvent) -> None:

    # Check that the received event is of the expected type, return error if not
    expected_type = "google.cloud.storage.object.v1.finalized"
    received_type = cloud_event["type"]
    if received_type != expected_type:
        raise ValueError(f"Expected {expected_type} but received {received_type}")

    # Extract the bucket and file names of the uploaded image for processing
    data = cloud_event.data
    bucket = data["bucket"]
    filename = data["name"]

    # Process the information in the new image
    detect_text(bucket, filename)

    print(f"File {filename} processed.")\


def detect_text(bucket: str, filename: str) -> None:

    print(f"Looking for text in image {filename}")

    # Use the Vision API to extract text from the image
    image = vision.Image(
        source=vision.ImageSource(gcs_image_uri=f"gs://{bucket}/{filename}")
    )
    text_detection_response = vision_client.text_detection(image=image)
    annotations = text_detection_response.text_annotations

    if annotations:
        text = annotations[0].description
    else:
        text = ""
    print(f"Extracted text {text} from image ({len(text)} chars).")

    detect_language_response = translate_client.detect_language(text)
    src_lang = detect_language_response["language"]
    print(f"Detected language {src_lang} for text {text}.")

    # Submit a message to the bus for each target language
    futures = []  # Asynchronous publish request statuses

    to_langs = os.environ.get("TO_LANG", "").split(",")
    for target_lang in to_langs:
        topic_name = os.environ.get("TRANSLATE_TOPIC")
        if src_lang == target_lang or src_lang == "und":
            topic_name = os.environ.get("RESULT_TOPIC")

        message = {
            "text": text,
            "filename": filename,
            "lang": target_lang,
            "src_lang": src_lang,
        }

        message_data = json.dumps(message).encode("utf-8")
        topic_path = publisher.topic_path(project_id, topic_name)
        future = publisher.publish(topic_path, data=message_data)
        futures.append(future)

    # Wait for each publish request to be completed before exiting
    for future in futures:
        future.result()

@functions_framework.cloud_event
def translate_text(cloud_event: CloudEvent) -> None:
    """Cloud Function triggered by PubSub when a message is received from
    a subscription.

    Translates the text in the message from the specified source language
    to the requested target language, then sends a message requesting another
    service save the result.
    """

    # Check that the received event is of the expected type, return error if not
    expected_type = "google.cloud.pubsub.topic.v1.messagePublished"
    received_type = cloud_event["type"]
    if received_type != expected_type:
        raise ValueError(f"Expected {expected_type} but received {received_type}")

    # Extract the message body, expected to be a JSON representation of a
    # dictionary, and extract the fields from that dictionary.
    data = cloud_event.data["message"]["data"]
    try:
        message_data = base64.b64decode(data)
        message = json.loads(message_data)

        text = message["text"]
        filename = message["filename"]
        target_lang = message["lang"]
        src_lang = message["src_lang"]
    except Exception as e:
        raise ValueError(f"Missing or malformed PubSub message {data}: {e}.")

    # Translate the text and publish a message with the translation
    print(f"Translating text into {target_lang}.")

    translated_text = translate_client.translate(
        text, target_language=target_lang, source_language=src_lang
    )

    topic_name = os.environ["RESULT_TOPIC"]
    message = {
        "text": translated_text["translatedText"],
        "filename": filename,
        "lang": target_lang,
    }
    message_data = json.dumps(message).encode("utf-8")
    topic_path = publisher.topic_path(project_id, topic_name)
    future = publisher.publish(topic_path, data=message_data)
    future.result()  # Wait for operation to complete

@functions_framework.cloud_event
def save_result(cloud_event: CloudEvent) -> None:
    """Cloud Function triggered by PubSub when a message is received from
    a subscription.

    Saves translated text to a Cloud Storage object as requested.
    """
    # Check that the received event is of the expected type, return error if not
    expected_type = "google.cloud.pubsub.topic.v1.messagePublished"
    received_type = cloud_event["type"]
    if received_type != expected_type:
        raise ValueError(f"Expected {expected_type} but received {received_type}")

    # Extract the message body, expected to be a JSON representation of a
    # dictionary, and extract the fields from that dictionary.
    data = cloud_event.data["message"]["data"]
    try:
        message_data = base64.b64decode(data)
        message = json.loads(message_data)

        text = message["text"]
        filename = message["filename"]
        lang = message["lang"]
    except Exception as e:
        raise ValueError(f"Missing or malformed PubSub message {data}: {e}.")

    print(f"Received request to save file {filename}.")

    # Save the translation in RESULT_BUCKET
    bucket_name = os.environ["RESULT_BUCKET"]
    result_filename = f"{filename}_{lang}.txt"
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(result_filename)

    print(f"Saving result to {result_filename} in bucket {bucket_name}.")

    blob.upload_from_string(text)

    print("File saved.")
