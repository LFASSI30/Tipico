# tipico.py

from google.colab import files
import os
from IPython.utils import io
import subprocess

# 1️⃣ Téléverser le fichier audio
uploaded = files.upload()
audio_file = list(uploaded.keys())[0]

# 2️⃣ Écrire le fichier sur le disque
with open(audio_file, "wb") as f:
    f.write(uploaded[audio_file])
del uploaded

# 3️⃣ Installer Whisper et ffmpeg via subprocess (sorties masquées)
with io.capture_output() as captured:
    subprocess.run(["pip", "install", "--upgrade", "openai-whisper"], check=True)
    subprocess.run(["apt", "update", "-y"], check=True)
    subprocess.run(["apt", "install", "ffmpeg", "-y"], check=True)

# 4️⃣ Afficher message de transcription
print("Transcription en cours, merci de ne pas fermer cette page. Vous pouvez mettre votre appareil en veille.")

# 5️⃣ Transcrire avec le modèle large
with io.capture_output() as captured:
    subprocess.run(["whisper", audio_file, "--model", "large"], check=True)

# 6️⃣ Préparer le nom du fichier texte généré
txt_file = os.path.splitext(audio_file)[0] + ".txt"

# 7️⃣ Télécharger automatiquement le fichier texte
files.download(txt_file)
