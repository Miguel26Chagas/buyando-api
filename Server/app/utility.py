import secrets
import string

def generate_secure_delivery_code(lenght = 6):
    return ''.join(secrets.choice(string.digits) for _ in range(lenght))

print(generate_secure_delivery_code())