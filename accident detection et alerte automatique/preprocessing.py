from PIL import Image
import numpy as np
import os

def resize_images(image_dir, target_size=(224, 224)):
    for filename in os.listdir(image_dir):
        filepath = os.path.join(image_dir, filename)
        try:
            img = Image.open(filepath)
            img = img.resize(target_size)
            img.save(filepath)
        except IOError:
            print(f"Impossible d'ouvrir ou de redimensionner l'image : {filepath}")

def normalize_images_01(image_dir):
    for filename in os.listdir(image_dir):
        filepath = os.path.join(image_dir, filename)
        try:
            img = Image.open(filepath)
            img_array = np.array(img, dtype=np.float32) / 255.0
            img_normalized = Image.fromarray((img_array * 255).astype(np.uint8))
            img_normalized.save(filepath)
        except IOError:
            print(f"Impossible d'ouvrir ou de normaliser l'image : {filepath}")
