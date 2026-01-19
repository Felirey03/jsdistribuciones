import os
import shutil
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__) + "/..")
DB_PATH = os.path.join(BASE_DIR, "instance", "jsdistribuciones.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

def backup_db():
    if not os.path.exists(DB_PATH):
        print("⚠️ No existe la base de datos, no se hizo backup")
        return

    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"jsdistribuciones_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_name)

    shutil.copy2(DB_PATH, backup_path)
    print(f"✅ Backup creado: {backup_path}")
