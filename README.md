# Huginn AI - Système de Reconnaissance Faciale

### Créé par Noah Herbelin-Alves

<img src="icon.png" alt="Huginn AI Logo" width="300"/>

## Description

**Huginn AI** est une application de reconnaissance faciale développée en Python utilisant les bibliothèques **OpenCV**, **face_recognition**, **DeepFace**, et **customtkinter** pour offrir une interface utilisateur intuitive. Le programme permet de détecter des visages en temps réel à partir d'un flux vidéo, d'analyser des traits spécifiques (comme l'âge, le genre, l'émotion et l'ethnie), et de comparer les visages détectés avec une base de données d'images de référence.

## Fonctionnalités

- **Reconnaissance faciale en temps réel** : Utilisation d'une webcam pour capturer les visages en direct et les comparer à une base de données d'images connues.
- **Analyse des traits faciaux** : Analyse de l'âge, du genre, des émotions et de l'ethnie des visages détectés grâce à **DeepFace**.
- **Interface utilisateur** : Une interface simple et ergonomique développée avec **customtkinter**, offrant des options de personnalisation comme le choix des thèmes et des périphériques de caméra.
- **Gestion de la base de données** : Chargement automatique des visages de référence à partir d'un répertoire spécifié.

> ⚠️ **Remarque :** Le projet n'est pas accessible sous forme de version web en raison de limitations techniques avec les bibliothèques utilisées. La fonctionnalité de recherche automatique des visages sur le web via **PimEyes** est en cours de développement et n'est pas encore disponible dans cette version.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les bibliothèques Python nécessaires :

- Python 3.8+
- OpenCV
- face_recognition
- numpy
- customtkinter
- Pillow
- DeepFace

### Installation des bibliothèques

```bash
pip install opencv-python face-recognition numpy customtkinter pillow deepface
```

## Installation

1. Clonez le dépôt
```bash
git clone https://github.com/justNoahH/Huginn-AI.git
```
2. Naviguez vers le dossier du projet :
```bash
cd huginn-ai
```
3. Assurez-vous que toutes les bibliothèques requises sont installées.
4. Exécutez l'application :
```bash
python main.py
```

## Utilisation

1. **Configurer le programme** : Choisir son périphérique vidéo et la base de données à comparer.
2. **Lancer le programme** : Cliquez sur "Démarrer" pour lancer la reconnaissance faciale en temps réel.
3. **Arrêter la reconnaissance** : Cliquez sur "Arrêter" pour interrompre le flux vidéo.
4. **Recherche de visage en ligne** : Cette fonctionnalité est en cours de développement.
5. **Analyse des traits faciaux** : En appuyant sur le bouton "Prédictions", l’application analysera les traits du visage actuellement capturé à l’aide de DeepFace.

## Structure du projet

```bash
huginn-ai/
│
├── main.py                 # Code principal de l'application
├── README.md               # Ce fichier
├── requirements.txt        # Liste des dépendances Python
├── icon.png                # Logo
└── base_de_donnees/        # Répertoire contenant les visages de référence
```

## Personnalisation
### Thèmes
L'application supporte les thèmes "Clair", "Sombre" et "Système". Vous pouvez changer de thème depuis le menu.

### Base de Données
Ajoutez des images au répertoire base_de_donnees/ pour qu'elles soient automatiquement incluses dans la base de données de visages connus. Les images doivent être au format .jpg ou .png.

## Dépendances et Limitations
### Compatibilité
Le projet est compatible avec les systèmes d'exploitation suivants :

- Windows
- macOS
- Linux

## Projets Futurs
- Intégration de la recherche de visages en ligne via PimEyes.
- Optimisation de l’algorithme de reconnaissance faciale pour une meilleure performance.
