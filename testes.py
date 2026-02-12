import secrets
import string

token = secrets.token_urlsafe(32)
# print(token)


def generate_secure_delivery_code():
    return ''.join(secrets.choice(string.digits) for _ in range(6))

print(generate_secure_delivery_code())