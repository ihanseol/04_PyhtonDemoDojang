import hashlib


def md5_hash(string):
    """Generate an MD5 hash for the given string."""
    hash_object = hashlib.md5(string.encode())
    return hash_object.hexdigest()


# Example usage
print(md5_hash("example string"))




