def user_db_get():
    with open('..database/database.txt') as f:
        return dict(f.readline())
user_db_get()