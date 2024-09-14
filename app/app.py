import streamlit as st
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import sklearn



################################ Optimisaion pour le chargement du modèle sauvegardé ##############################

import pickle
import os

@st.cache_resource
def load_model(model_path):
    """ Fonction pour charger un modèle à partir d'un fichier .pkl """
    if not os.path.exists(model_path):
        st.error(f"Erreur : Le fichier {model_path} est introuvable.")
        return None
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle : {e}")
        return None

# Chargement du modèle
model_tree = load_model('model_tree.pkl')

if model_tree is None:
    st.stop()  # Arrête l'application si le modèle n'a pas pu être chargé
    
   

########################################################################



# CSS pour ajouter une image d'arrière-plan
st.markdown('''
    <style>
    .stApp {
        background-image: url("https://www.cardiologie-pratique.com/sites/www.cardiologie-pratique.com/files/styles/une_journal_578_383/public/images/article_journal/poinsignon-cardiovasculaire_600459379_1.png?itok=FQv6uxM-");
        background-size: cover;
        background-position: center;
    }
    </style>
''', unsafe_allow_html=True)

# Titre de l'application
st.title("FKS (Falilou, Khardiata et Salif) APPlication de Prédiction de la présence de maladie cardiaque")

# Informations personnelles du patient
st.write("Veuillez entrer vos informations personnelles :")
nom = st.text_input('Nom')
prenom = st.text_input('Prénom')
adresse = st.text_input('Adresse')
telephone = st.text_input('Numéro de téléphone')

# Instructions pour l'utilisateur
st.write("Entrez les caractéristiques du patient pour prédire la présence d'une maladie cardiaque.")

# Variables d'entrée
age = st.number_input('Âge (en années)', min_value=1, max_value=120, value=30)
sexe = st.selectbox('Sexe', options=[('Homme', 1), ('Femme', 0)])
cp = st.selectbox('Type de douleur thoracique (CP)', options=[1, 2, 3, 4])
trestbps = st.number_input('Pression artérielle au repos (TRESTBPS) (en mm Hg)', min_value=50, max_value=200, value=120)
chol = st.number_input('Cholestérol sérique (CHOL) (en mg/dl)', min_value=100, max_value=600, value=200)
fps = st.selectbox('Glycémie à jeun > 120 mg/dl (FPS)', options=[('Oui', 1), ('Non', 0)])
restech = st.selectbox('Résultats électrocardiographiques au repos (RESTECH)', options=[0, 1, 2])
thalach = st.number_input('Fréquence cardiaque maximale atteinte (THALACH)', min_value=60, max_value=220, value=150)
exang = st.selectbox('Angine induite par l\'exercice (EXANG)', options=[('Oui', 1), ('Non', 0)])
oldpeak = st.number_input('Dépression ST induite par l\'exercice (OLDPEAK)', min_value=0.0, max_value=10.0, value=1.0, step=0.1)
slope = st.selectbox('Pente du segment ST (SLOPE)', options=[1, 2, 3])
ca = st.number_input('Nombre de vaisseaux principaux colorés par flouroscopie (CA)', min_value=0, max_value=3, value=0)
thal = st.selectbox('THAL (1 = normal ; 2 = défaut fixe ; 3 = défaut réversible)', options=[1, 2, 3])

# Prédiction à partir des variables d'entrée
input_data = np.array([[age, sexe[1], cp, trestbps, chol, fps[1], restech, thalach, exang[1], oldpeak, slope, ca, thal]])
prediction = model_tree.predict(input_data)

# Affichage du résultat de la prédiction
result = "Maladie cardiaque" if prediction[0] == 1 else "Pas de maladie cardiaque"
st.success(f"Le modèle prédit que le patient est atteint de {result}.")

# Enregistrement des données
if st.button('Enregistrer la consultation'):
    # Récupérer la date et l'heure actuelles
    consultation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Création d'un dictionnaire avec les données à enregistrer
    data = {
        'Nom': nom,
        'Prénom': prenom,
        'Adresse': adresse,
        'Téléphone': telephone,
        'Âge': age,
        'Sexe': 'Homme' if sexe[1] == 1 else 'Femme',
        'CP': cp,
        'TRESTBPS': trestbps,
        'CHOL': chol,
        'FPS': 'Oui' if fps[1] == 1 else 'Non',
        'RESTECH': restech,
        'THALACH': thalach,
        'EXANG': 'Oui' if exang[1] == 1 else 'Non',
        'OLDPEAK': oldpeak,
        'SLOPE': slope,
        'CA': ca,
        'THAL': thal,
        'Résultat': result,
        'Date et Heure de consultation': consultation_time,
        #'Structure Sanitaire': structures
    }
    
    # Convertir les données en DataFrame et les enregistrer dans un fichier CSV
    pd.DataFrame([data]).to_csv('consultations.csv', mode='a', header=False, index=False)
    
    st.success("Les données de consultation ont été enregistrées avec succès.")

# Identifiants du cardiologue
st.sidebar.title("Identifiants du Cardiologue")
cardiologue_nom = st.sidebar.text_input("Nom du Cardiologue")
cardiologue_mdp = st.sidebar.text_input("Mot de passe", type="password")

# Structure sanitaire du cardiologue
st.sidebar.write("Choisissez votre structure sanitaire :")
structures = [
    'Hôpital Principal de Dakar', 'Clinique la Croix Bleue Castors', 'Centre Médical Mame Abdoul Aziz Parcelles Assainies',
    'Hôpital Matlabul Fawzeyni Touba', 'Centre de Santé CHIIFA Parcelles Assainies'
]
structure_sanitaire = st.sidebar.selectbox('Structure Sanitaire', options=structures)

# Bouton de connexion
if st.sidebar.button('Se Connecter'):
    if cardiologue_nom and cardiologue_mdp:
        st.sidebar.success("Connexion réussie!")
        # Code pour valider les identifiants ou gérer la session de connexion peut être ajouté ici
    else:
        st.sidebar.error("Veuillez entrer le nom et le mot de passe du cardiologue.")

# Bas de page
st.markdown("---")
st.markdown("#### © 2024 Mohamed Falilou Fall , Khardiata Ke Faye , Mamadou Salif Diallo- Application de Prédiction de la Maladie Cardiaque")
st.markdown("##### Contact : mff.faliou.fall@gmail.com | khardiatakefaye@gmail.com | mamadousalif.diallo@uadb.edu.sn")

