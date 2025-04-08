import random
import os

def get_random_image(image_dir):
    return random.choice(os.listdir(image_dir))


# import streamlit as st
# from PIL import Image
# import numpy as np
# import torch
# from datetime import datetime
# from fastai.vision.all import *
# from model import label_function

# # Charger le modèle
# learn = load_learner('accident_detection.pkl')

# # Sidebar
# st.sidebar.title("Options")
# option = st.sidebar.selectbox("Choisissez une option", ["Uploader une image"])

# # Fonction pour uploader une image et tester le modèle
# def uploader_image():
#     st.header("Uploader une image")
#     uploaded_file = st.file_uploader("Choisissez une image", type=["jpeg", "png", "jpg"])
#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         st.image(image, caption="Image uploadée", use_container_width=True)
        
#         # Prétraitement de l'image
#         image = image.resize((224, 224))
#         image_array = np.array(image, dtype=np.float32) / 255.0
#         # image_tensor = torch.tensor(image_array).permute(2, 0, 1).unsqueeze(0)  # Convertir en torch.Tensor
        
#         # Prédiction
#         is_accident, _, probs = learn.predict(image)
#         st.write(f"C'est une scène de : {is_accident}.")
#         st.write(f"Probabilité d'accident: {probs[0]:.4f}")
        
#         if is_accident == "accident":
#             st.error("Accident détecté!")
#             st.write(f"Date et heure: {datetime.now()}")
#             st.write("Lieu: Abidjan, Côte d'Ivoire")

# # Afficher l'option choisie
# if option == "Uploader une image":
#     uploader_image()
