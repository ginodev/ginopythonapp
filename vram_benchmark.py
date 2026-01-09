# File: vram_benchmark.py
# Descrizione: Script per il benchmark della VRAM e test di caricamento del modello Whisper su GPU NVIDIA.

import torch
import gc
import sys
import time

def print_vram_status(label="Status"):
    """
    Stampa lo stato attuale della memoria VRAM utilizzata e libera.
    """
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**2
        reserved = torch.cuda.memory_reserved() / 1024**2
        free_in_device = torch.cuda.get_device_properties(0).total_memory / 1024**2 - (reserved)
        print(f"--- {label} ---")
        print(f"Allocata: {allocated:.2f} MB")
        print(f"Riservata: {reserved:.2f} MB")
        print(f"Libera stimata: {free_in_device:.2f} MB")
        print("-" * (len(label) + 8))
    else:
        print("CUDA non disponibile.")

def run_benchmark():
    """
    Esegue il benchmark completo caricando le librerie e simulando l'allocazione del modello.
    """
    print("Inizio Benchmark VRAM per Whisper...")
    
    if not torch.cuda.is_available():
        print("ERRORE: CUDA non è rilevato. Controlla i driver o l'installazione di PyTorch.")
        return

    device_name = torch.cuda.get_device_name(0)
    total_mem = torch.cuda.get_device_properties(0).total_memory / 1024**2
    print(f"Dispositivo rilevato: {device_name}")
    print(f"VRAM Totale: {total_mem:.2f} MB")
    
    print_vram_status("Iniziale (Idle)")

    try:
        # Importazione di Whisper (richiede openai-whisper o faster-whisper)
        print("\nCaricamento libreria Whisper...")
        import whisper
        
        # Test 1: Caricamento modello Large-v3
        model_name = "large-v3"
        print(f"\nTentativo di caricamento modello: {model_name}...")
        start_time = time.time()
        
        # Nota: La GTX 1660 Super ha 6GB. Large-v3 richiede circa 3GB solo per i pesi.
        # Con il sistema operativo e altri processi, il margine è stretto.
        model = whisper.load_model(model_name, device="cuda")
        
        end_time = time.time()
        print(f"Modello {model_name} caricato con successo in {end_time - start_time:.2f}s!")
        print_vram_status(f"Dopo caricamento {model_name}")
        
        # Test di inferenza rapida (opzionale - dummy data)
        print("\nEsecuzione test inferenza rapida (zero-signal)...")
        # dummy audio 30s
        # model.transcribe(...) 

    except torch.cuda.OutOfMemoryError:
        print(f"\nERRORE: Memoria VRAM insufficiente per {model_name}!")
        print("Suggerimento: Chiudi applicazioni che usano la GPU (browser, wallpaper engine, etc.)")
    except Exception as e:
        print(f"\nSi è verificato un errore inaspettato: {e}")
    finally:
        # Pulizia per evitare blocchi
        if 'model' in locals():
            del model
        gc.collect()
        torch.cuda.empty_cache()
        print("\nCache CUDA svuotata.")
        print_vram_status("Finale (Dopo pulizia)")

if __name__ == "__main__":
    # Avvio del benchmark
    run_benchmark()