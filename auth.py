import bcrypt
def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
        # Convert both strings to bytes to perform the check
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

h1 = hash_password("test123")
h2 = hash_password("test123")
print(h1)
print(h2)
print(h1 == h2)
print(verify_password("test123", h1))
print(verify_password("wrongpassword", h1))