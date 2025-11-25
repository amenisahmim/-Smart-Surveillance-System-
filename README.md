# Projet Reconnaissance Faciale Raspberry Pi

---

## Description

Ce projet implémente un système de reconnaissance faciale en temps réel sur **Raspberry Pi** utilisant **OpenCV**.  
Il permet de détecter et reconnaître des visages à partir de la caméra du Raspberry Pi et de gérer un petit dataset pour l'entraînement.

---

## Fonctionnalités

- Détection de visage en temps réel  
- Reconnaissance faciale personnalisée avec dataset utilisateur  
- Capture d’images depuis le Raspberry Pi  
- Entraînement du modèle localement  
- Possibilité d’ajouter facilement de nouvelles personnes au dataset

---

## Prérequis / Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/amenisahmim/Raspberry-Pi-face-recognition.git
cd Raspberry-Pi-face-recognition
Installer Python 3.x et pip si ce n’est pas déjà fait.

2. Installer les dépendances Python :

pip install -r requirements.txt


Activer la caméra sur Raspberry Pi et connecter la caméra si nécessaire.
3. Structure du projet
FaceRecognition/
│── face_recognition_phone.py          # Script principal pour la reconnaissance faciale
│── facial_recognition_hardware.py    # Script pour intégration avec hardware spécifique
│── image_capture.py                   # Script pour capturer des images depuis la caméra
│── model_training.py                  # Script pour entraîner le modèle avec le dataset
│── phoneCAM.py                        # Script spécifique pour caméra de téléphone
│── dataset/                           # Contient les images des personnes pour entraînement
│── encodings.pickle                   # Fichier généré après l'entraînement
│── requirements.txt                   # Dépendances Python
│── README.md                          # Ce fichier
│── .gitignore                         # Fichiers et dossiers à ignorer par Git
│── licenses/                          # Licences des bibliothèques utilisées

4. Utilisation

Ajouter des images dans dataset/nom_personne/.

Générer les encodages :

python model_training.py


Lancer la reconnaissance faciale :

python face_recognition_phone.py

Licence

Projet libre. Licences des bibliothèques incluses dans licenses/.




