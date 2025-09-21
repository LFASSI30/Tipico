# tipico_fast.py

import os
from IPython.utils import io
import subprocess
from google.colab import files

# 1️⃣ Placer le fichier audio dans l'espace de travail Colab manuellement
# Exemple : tu mets ton fichier audio dans /content/audio.mp3
audio_file = "audio.mp3"  # change ce nom si besoin

if not os.path.exists(audio_file):
    print(f"⚠️ Le fichier {audio_file} n'existe pas dans /content. Veuillez l'uploader manuellement.")
else:
    print(f"✅ Fichier trouvé : {audio_file}")

    # 2️⃣ Installer Whisper et ffmpeg (sorties masquées)
    with io.capture_output() as captured:
        subprocess.run(["pip", "install", "--upgrade", "openai-whisper"], check=True)
        subprocess.run(["apt", "update", "-y"], check=True)
        subprocess.run(["apt", "install", "ffmpeg", "-y"], check=True)

    # 3️⃣ Transcrire avec le modèle large
    with io.capture_output() as captured:
        subprocess.run(["whisper", audio_file, "--model", "large"], check=True)

    # 4️⃣ Préparer le nom du fichier texte généré
    txt_file = os.path.splitext(audio_file)[0] + ".txt"

    # 5️⃣ Télécharger automatiquement le fichier texte
    if os.path.exists(txt_file):
        files.download(txt_file)
    else:
        print("⚠️ La transcription n'a pas généré de fichier texte.")
