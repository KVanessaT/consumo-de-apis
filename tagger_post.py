import requests
import json
import shutil
import os

api_key = 'acc_8370c473e2810a6'
api_secret = 'e9cf622303435217db7dc4cd2530ad88'
image_dir = 'imagenes/'

CLASSIFICATION_PATH = 'imagenes/clasificacion/'
CATEGORIES = ['tree', 'plant']
FILE_SEP = os.sep


def checkPaths(categories, classification_path):
    if not os.path.exists(classification_path):
            os.mkdir(classification_path)
    for category in categories:
        target_path = classification_path+category+FILE_SEP
        if not os.path.exists(target_path+category+FILE_SEP):
            os.mkdir(target_path)


def classifyImage(image_path, categories, classification_path):
    response = requests.post(
        'https://api.imagga.com/v2/tags',
        auth=(api_key, api_secret),
        files={'image': open(image_path, 'rb')}
    )
    if response.status_code == 200:
        data = response.json()
        filename = image_path.split(FILE_SEP)[1]
        for tag in data['result']['tags']:
            for category in categories:
                target_path = classification_path+FILE_SEP+category+FILE_SEP
                if (tag['confidence'] == 100 and tag['tag']['en'] == category):
                    shutil.copy(image_path, target_path+filename)
    else:
        print("API error "+image_path)


checkPaths(CATEGORIES, CLASSIFICATION_PATH)

for filename in os.listdir(image_dir):
    f = os.path.join(image_dir, filename)
    if os.path.isfile(f):
        image_path = os.path.splitext(f)[0] + os.path.splitext(f)[1]
        classifyImage(image_path, CATEGORIES, CLASSIFICATION_PATH)
