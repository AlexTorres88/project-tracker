import bcrypt

def hash_password(password: str):
    return bcrypt.hashpw(password, bcrypt.gensalt())

def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password, hashed_password)