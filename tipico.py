# tipico.py
# Version : streaming live des logs Whisper dans Colab

from google.colab import files
import os
import subprocess
import sys
import shutil
import time

# 1️⃣ Téléverser le fichier audio (interface Colab)
uploaded = files.upload()
audio_file = list(uploaded.keys())[0]

# 2️⃣ Écrire le fichier sur le disque
with open(audio_file, "wb") as f:
    f.write(uploaded[audio_file])
del uploaded

# Helper : exécute silencieusement une commande, mais retombe en mode verbeux si échec
def run_silent(cmd, name=None):
    name = name or " ".join(cmd)
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"[!] La commande `{name}` a échoué — affichage de la sortie pour debug:")
        subprocess.run(cmd, check=True)

# 3️⃣ Installer Whisper et ffmpeg (silencieux sauf en cas d'erreur)
run_silent([sys.executable, "-m", "pip", "install", "--upgrade", "openai-whisper"], "pip install openai-whisper")
run_silent(["apt", "update", "-y"], "apt update")
run_silent(["apt", "install", "-y", "ffmpeg"], "apt install ffmpeg")

# 4️⃣ Préparer la commande whisper (vérifie d'abord si 'whisper' existe)
if shutil.which("whisper") is not None:
    whisper_cmd = ["whisper", audio_file, "--model", "large"]
else:
    # essaie d'exécuter via python -m whisper si la commande n'est pas trouvée
    whisper_cmd = [sys.executable, "-m", "whisper", audio_file, "--model", "large"]

print("Lancement de la transcription — affichage en direct des logs :\n")

# 5️⃣ Lancer whisper et streamer sa sortie en temps réel
proc = subprocess.Popen(
    whisper_cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    bufsize=1
)

# Lecture robuste en temps réel (gestion buffering / carriage returns)
try:
    while True:
        line = proc.stdout.readline()
        if line:
            # Affiche exactement ce que Whisper envoie (sans double saut)
            print(line, end="")
        elif proc.poll() is not None:
            # plus rien et processus terminé
            break
        else:
            # pas encore de sortie, on attend un peu
            time.sleep(0.05)
finally:
    # assure la fin du process
    proc.wait()

if proc.returncode != 0:
    print(f"\n[!] Whisper s'est terminé avec le code {proc.returncode}")

# 6️⃣ Préparer le nom du fichier texte généré et télécharger
txt_file = os.path.splitext(audio_file)[0] + ".txt"
if os.path.exists(txt_file):
    files.download(txt_file)
else:
    print(f"\n[!] Fichier de sortie attendu '{txt_file}' non trouvé.")
