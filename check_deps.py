# File: check_deps.py
# Descrizione: Script per verificare la presenza delle dipendenze necessarie alla gestione dei formati file.

import sys
import importlib

def check_dependencies():
    """
    Controlla se i moduli necessari per .txt, .srt, .json e .docx sono installati.
    """
    # txt, json, srt (implementato custom) usano librerie standard o logica nativa
    # docx richiede python-docx
    dependencies = {
        "json": "json (Standard Library)",
        "docx": "python-docx",
        "requests": "requests (Richiesta per API Gemini)"
    }
    
    print("--- Verifica Dipendenze Python ---")
    missing = []
    
    for key, lib in dependencies.items():
        try:
            # Per python-docx il nome del modulo è 'docx'
            module_name = 'docx' if key == 'docx' else key
            importlib.import_module(module_name)
            print(f"[OK] {lib} è installata correttamente.")
        except ImportError:
            print(f"[MANCANTE] {lib} NON è installata.")
            missing.append(lib)
            
    if missing:
        print("\nPer installare le librerie mancanti, esegui il seguente comando nel terminale:")
        # Uso 'py' come richiesto dalle tue istruzioni per l'ambiente Windows/Python aggiornato
        libs_to_install = " ".join([m.split(" ")[0] for m in missing])
        print(f"py -m pip install {libs_to_install}")
    else:
        print("\nTutte le librerie necessarie sono presenti.")

if __name__ == "__main__":
    check_dependencies()