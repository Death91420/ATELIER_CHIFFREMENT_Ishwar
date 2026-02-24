import os
import sys
from nacl.secret import SecretBox
from nacl.utils import random

def get_box():
    # SecretBox a besoin d'une clé de 32 octets.
    # On la récupère depuis une variable d'environnement dédiée.
    key_env = os.getenv("NACL_SECRET_KEY")
    
    if not key_env:
        print("❌ Erreur : NACL_SECRET_KEY non définie.")
        sys.exit(1)
    
    # On s'assure que la clé fait 32 octets (on encode et on tronque/complète si besoin)
    key_bytes = key_env.encode('utf-8')[:32].ljust(32, b'\0')
    return SecretBox(key_bytes)

def process_file(action, input_path, output_path):
    box = get_box()
    
    try:
        with open(input_path, 'rb') as f:
            data = f.read()

        if action == "encrypt":
            # SecretBox.encrypt génère un 'nonce' (sel) unique automatiquement
            processed_data = box.encrypt(data)
            msg = "chiffré"
        elif action == "decrypt":
            processed_data = box.decrypt(data)
            msg = "déchiffré"
        else:
            print("Action invalide.")
            return

        with open(output_path, 'wb') as f:
            f.write(processed_data)
        print(f"✅ Succès PyNaCl : {input_path} {msg} dans {output_path}")

    except Exception as e:
        print(f"❌ Erreur lors de l'opération : {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python app/nacl_crypto.py [encrypt/decrypt] <source> <destination>")
    else:
        process_file(sys.argv[1], sys.argv[2], sys.argv[3])