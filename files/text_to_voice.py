#text_to_voice

import os
from unicodedata import name
from urllib import response
from google.cloud import texttospeech_v1
from text_detection import textT

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='*shentai_file.json'
client=texttospeech_v1.texttospeechclient()

text=textT

synthesis_input= texttospeech_v1.synthesisInput(ssml=text)

voice1=texttospeech_v1.voiceselectionparams (
    language_code='en-in',
    ssml_gender=texttospeech_v1.SsmlVoiceGender.MALE    
)

voice2=texttospeech_v1.voiceselectionparams (
    name='vi-VN-Wavenet-D',
    language_code='vi-VN'
)

print(client.list_voices)
audio_config= texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.audioencoding.mp3
)

response1=client.synthesize_speech (
    input=synthesis_input,
    voices= voice1,
    audio_config=audio_config    
)

with open('audio.mp3', 'wb') as output:
    output.write(response1.audio_content)

