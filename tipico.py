from google.colab import files
import os

# --- Ton code normal ---
# 1️⃣ Téléverser le fichier audio
uploaded = files.upload()

# Récupérer le nom du fichier téléversé
audio_file = list(uploaded.keys())[0]

# 2️⃣ Écrire le fichier sur le disque pour libérer la RAM
with open(audio_file, "wb") as f:
    f.write(uploaded[audio_file])

# Libérer la variable upload pour réduire la mémoire utilisée
del uploaded

# 3️⃣ Installer Whisper et ffmpeg si nécessaire (sorties visibles)
!pip install --upgrade openai-whisper
!sudo apt update && sudo apt install ffmpeg -y

# 4️⃣ Transcrire avec le modèle large (sorties visibles)
!whisper "{audio_file}" --model large

# 5️⃣ Préparer le nom du fichier texte généré
txt_file = os.path.splitext(audio_file)[0] + ".txt"

# 6️⃣ Télécharger automatiquement le fichier texte
files.download(txt_file)
