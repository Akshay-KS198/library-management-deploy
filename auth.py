users_db = {
    "admin1": "admin",
    "user1": "user",
    "user2": "user"
}

def get_user_role(username):
    return users_db.get(username)