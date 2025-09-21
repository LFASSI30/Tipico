# tipico.py

import os
import subprocess
from google.colab import files

# 1️⃣ Identifier le fichier audio dans l'espace de travail
audio_extensions = [".mp3", ".wav", ".m4a", ".flac", ".ogg"]
all_files = os.listdir()  # liste tous les fichiers dans le dossier courant
audio_files = [f for f in all_files if os.path.splitext(f)[1].lower() in audio_extensions]

if len(audio_files) == 0:
    raise FileNotFoundError("Aucun fichier audio trouvé dans l'espace de travail.")
elif len(audio_files) > 1:
    raise Exception("Plusieurs fichiers audio trouvés. Assurez-vous qu'il n'y ait qu'un seul fichier audio.")
else:
    audio_file = audio_files[0]

print(f"Fichier audio trouvé : {audio_file}")

# 2️⃣ Installer Whisper et ffmpeg (sorties masquées)
import IPython.utils.io as io
with io.capture_output() as captured:
    subprocess.run(["pip", "install", "--upgrade", "openai-whisper"], check=True)
    subprocess.run(["apt", "update", "-y"], check=True)
    subprocess.run(["apt", "install", "ffmpeg", "-y"], check=True)

# 3️⃣ Transcrire avec Whisper en affichage temps réel
print("\nTranscription en cours, merci de ne pas fermer cette page 44444...\n")
get_ipython().system(f'whisper "{audio_file}" --model large')

# 4️⃣ Préparer le nom du fichier texte généré
txt_file = os.path.splitext(audio_file)[0] + ".txt"

# 5️⃣ Télécharger automatiquement le fichier texte
files.download(txt_file)
