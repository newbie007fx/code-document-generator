

import zipfile
import os
from typing import List, Tuple

class CodeReader:
    def __init__(self, extract_path: str = "extracted_code"):
        self.extract_path = extract_path
        os.makedirs(self.extract_path, exist_ok=True)

    def extract_zip(self, zip_file_path: str) -> str:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_path)
        return self.extract_path

    def read_code_files(self, extensions: Tuple[str, ...] = ('.py', '.go', '.js', '.ts', '.php')) -> List[Tuple[str, str]]:
        code_files = []
        for root, _, files in os.walk(self.extract_path):
            for file in files:
                if file.startswith(('_', '.')):
                    continue
                if file.endswith(extensions):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            rel_path = os.path.relpath(full_path, self.extract_path)
                            code_files.append((rel_path, content))
                    except Exception as e:
                        print(f"Error reading {full_path}: {e}")
        return code_files