import bcrypt

def hash_password(password: str):
    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hash.decode('utf-8')

def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf8'), hashed_password)