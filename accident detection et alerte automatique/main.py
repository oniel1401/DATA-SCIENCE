import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
from fastai.vision.all import *
from model import label_function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import io
import pathlib
import platform


#Windows
if platform.system() == 'Windows':
    pathlib.PosixPath = pathlib.WindowsPath

from fastai.vision.all import *
learn = load_learner('accident3_detection.pkl')

# #modèle
# learn = load_learner('accident3_detection.pkl')

#envoie de mail
def envoyer_email(subject, body, to_email, image_path):
    from_email = "lamifaeffi@gmail.com"
    password = "itby jnxl krfs smxq"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    #ajout d'image
    with open(image_path, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name=os.path.basename(image_path))
    msg.attach(image)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

#Sidebar
st.sidebar.title("Options")
option = st.sidebar.selectbox("Choisissez une option", ["Uploader une image"])

#uploader image
def uploader_image():
    st.header("Uploader une image")
    uploaded_file = st.file_uploader("Choisissez une image", type=["jpeg", "png", "jpg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Image uploadée", use_container_width=True)
        
        # Sauvegarder l'image uploadée
        image_path = "uploaded_image.jpg"
        image.save(image_path)
        
        # Prétraitement de l'image
        image = image.resize((224, 224))
        image_array = np.array(image, dtype=np.float32) / 255.0
        image_tensor = torch.tensor(image_array).permute(2, 0, 1).unsqueeze(0)
        
        # Prédiction
        is_accident, _, probs = learn.predict(image)
        st.write(f"C'est une scène de : {is_accident}.")
        st.write(f"Probabilité d'accident: {probs[0]:.4f}")
        
        if is_accident == "accident":
            st.error("Accident détecté!")
            st.write(f"Date et heure: {datetime.now()}")
            st.write("Lieu: Abidjan, Côte d'Ivoire")
            
            # Envoyer une alerte par email avec l'image
            subject = "Alerte d'accident détecté"
            body = f"Un accident a été détecté.\nDate et heure: {datetime.now()}.\nLieu: Abidjan, Côte d'Ivoire.\nProbabilité: {probs[0]:.4f}"
            envoyer_email(subject, body, "onielbusiness14@gmail.com", image_path)

# Afficher
if option == "Uploader une image":
    uploader_image()
