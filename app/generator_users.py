import random
import string


def generate_email(domain: str = "gmail.com"):
    users = []
    for _ in range(10):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(15))
        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(15))
        email = f"{username}@{domain}"
        users.append({
            'username': username,
            'email': email,
            'pass': password
        })

    return users
