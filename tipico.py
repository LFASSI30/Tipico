from google.colab import files
import os

# Téléverser le fichier audio
uploaded = files.upload()
audio_file = list(uploaded.keys())[0]

# Sauvegarder le fichier
with open(audio_file, "wb") as f:
    f.write(uploaded[audio_file])
del uploaded

# Préparer le nom du fichier texte généré
txt_file = os.path.splitext(audio_file)[0] + ".txt"

# Télécharger automatiquement le fichier texte
files.download(txt_file)
