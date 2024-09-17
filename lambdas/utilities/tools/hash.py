import hashlib


def hash_file(filename: str) -> str:
    with open(filename, "rb", buffering=0) as f:
        return hashlib.file_digest(f, "sha256").hexdigest()
