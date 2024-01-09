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


def split_users(users: list[dict], spliter: int):
    length = len(users)
    split_n = length // spliter if length % spliter == 0 else (length // spliter) + 1
    data_users = []
    i = 0
    while split_n > 0:
        data_users.append(
            users[i:i+spliter]
        )
        i = i+spliter
        split_n -= 1
    return data_users
