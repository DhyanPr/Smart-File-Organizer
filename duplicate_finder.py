import hashlib

def get_file_hash(file_path):
    hasher = hashlib.md5()

    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()

    except Exception as e:
        print(f"Hashing failed for {file_path}: {e}")  # 👈 ADD THIS
        return None