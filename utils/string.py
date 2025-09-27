import bcrypt

def verify(plain_value, hashed_value):
    value_bytes = plain_value.encode('utf-8')
    hashed_value_bytes = hashed_value.encode('utf-8')
    return bcrypt.checkpw(value_bytes, hashed_value_bytes)

def hash(value):
    value_bytes = value.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_value = bcrypt.hashpw(value_bytes, salt)
    return hashed_value.decode('utf-8')

def coalesce(value, fallback):
    return value if value is not None else fallback
