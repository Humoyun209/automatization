def read_users(path_name):
    users = []

    with open(path_name, "r") as f:
        for user in f.read().strip().split("\n"):
            users.append(
                {
                    "email": user.strip().split(":")[0],
                    "username": user.strip().split(":")[0].split("@")[0],
                    "pass": user.strip().split(":")[1],
                }
            )
    return users