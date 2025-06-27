import os
import shutil

def cleanup_folder(path: str):
    """Deletes the folder and recreates it empty."""
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


