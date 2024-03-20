#!/usr/bin/python3

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
import os
import glob
import sys
import binascii
import argparse
from itertools import islice
from pathlib import Path

from minio import Minio

app = Flask("Flask Image Gallery")
app.config['IMAGE_EXTS'] = [".png", ".jpg", ".jpeg", ".gif", ".tiff"]
app.config['IMAGE_EXTSS'] = ["*.png", "*.jpg", "*.jpeg", ".gif", ".tiff"]
app.config['path'] = r".\Flask-Image-Gallery-master"

MAX_IMGS = 10



root_path = Path(__file__).parent
# print(root_path)

def encode(x):
    return binascii.hexlify(x.encode('utf-8')).decode()

def decode(x):
    return binascii.unhexlify(x.encode('utf-8')).decode()


@app.route('/')
def home():
    list_images_incurret_folder()
    image_paths = []
    images_list =  []
    fetchimagesfromminio()
    images_path = Path(root_path).joinpath('rat-images')
    for extension in app.config['IMAGE_EXTSS']:
        images_list.extend(list(Path(images_path).glob(extension)))

    image_paths =  [encode(str(p.resolve())) for p in images_list]
    
    return render_template('index.html', paths=image_paths)


@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir,filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)

def fetchimagesfromminio():
    try:
        client = Minio(
        "192.168.178.42:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False,
        )

        # List objects information.
        images_path = Path(root_path).joinpath('rat-images')
        objects = client.list_objects("cloudcomputing")
        objects =  sorted(objects, reverse=True, key=lambda a: a.last_modified)
        objects =  islice(objects,  MAX_IMGS)
        for obj in objects:
            client.fget_object("cloudcomputing", obj.object_name, Path(images_path).joinpath(obj.object_name))
    except Exception as e:
        print(e)



def list_images_incurret_folder():

    images_list = []
    images_path = Path(root_path).joinpath('rat-images')
    archive_path = Path(root_path).joinpath('images-archive')
    for extension in app.config['IMAGE_EXTSS']:
        images_list.extend(list(Path(images_path).glob(extension)))

    images_list = sorted(images_list, key=os.path.getmtime)

    if len(images_list) > MAX_IMGS:
        for arc_img in images_list[MAX_IMGS:]:
            new_location =  Path(archive_path).joinpath(arc_img.name)
            Path(arc_img).rename(new_location)
            print("moved")




if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
