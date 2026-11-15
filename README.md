# ChronoOverlay

Une horloge de bureau flottante, minimaliste et futuriste pour Windows.

## Fonctionnalités
- Heure numérique au format 24 h avec secondes.
- Date complète en français.
- Fenêtre sans bordure, toujours au premier plan.
- Effet Liquid Glass avec transparence et arrière-plan Acrylic natif sous Windows 11.
- Déplacement par glisser-déposer.
- Mode compact.
- Réglage rapide de la transparence par clic droit.
- Icône dans la zone de notification : double-clic pour afficher/masquer, menu pour quitter.

## Installation et lancement
1. Installer Python 3.10 ou plus récent.
2. Ouvrir un terminal dans ce dossier.
3. Exécuter :
   ```bash
   py -m pip install -r requirements.txt
   py main.py
   ```

## Créer un exécutable Windows (.exe)
Dans le même dossier :
```bash
py -m pip install pyinstaller
py -m PyInstaller --noconfirm --onefile --windowed --name ChronoOverlay main.py
```
L'exécutable sera créé dans `dist/ChronoOverlay.exe`.

## Utilisation
- Glisser la fenêtre pour la déplacer.
- Clic droit sur la fenêtre pour régler la transparence.
- Bouton « — » pour passer en mode compact.
- Bouton « × » pour quitter.
- Double-cliquer sur l'icône de notification pour afficher/masquer.

## Obtenir le fichier .exe sans installer Python sur votre PC

Le dossier `.github/workflows` contient un automatisme de compilation Windows via GitHub Actions.
Python et PyInstaller seront installés uniquement sur la machine de compilation distante, pas sur le PC qui exécutera l'application.

1. Créez un compte sur https://github.com si nécessaire.
2. Créez un dépôt GitHub vide.
3. Importez-y tous les fichiers de ce projet, y compris le dossier caché `.github`.
4. Dans le dépôt, ouvrez l'onglet **Actions**.
5. Sélectionnez **Build ChronoOverlay for Windows**, puis **Run workflow**.
6. Une fois l'exécution terminée, ouvrez-la et téléchargez l'artefact **ChronoOverlay-Windows**.
7. Décompressez l'archive téléchargée : vous obtiendrez `ChronoOverlay.exe`.

Vous pourrez ensuite lancer `ChronoOverlay.exe` sur Windows sans installer Python ni PySide6.
