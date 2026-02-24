import os
import sys
from cryptography.fernet import Fernet

def get_cipher():
    # Récupère la clé stockée dans le Secret GitHub (injectée en variable d'env)
    key = os.getenv("MY_GITHUB_SECRET_KEY")
    if not key:
        print("❌ Erreur : La variable MY_GITHUB_SECRET_KEY n'est pas définie.")
        sys.exit(1)
    return Fernet(key.encode())

def process_file(action, input_file, output_file):
    cipher = get_cipher()
    try:
        with open(input_file, 'rb') as f:
            data = f.read()
        
        if action == "encrypt":
            result = cipher.encrypt(data)
        else:
            result = cipher.decrypt(data)
            
        with open(output_file, 'wb') as f:
            f.write(result)
        print(f"✅ Succès : {input_file} -> {output_file}")
    except Exception as e:
        print(f"❌ Erreur lors du {action} : {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python fernet_atelier1.py [encrypt/decrypt] <input> <output>")
    else:
        process_file(sys.argv[1], sys.argv[2], sys.argv[3])