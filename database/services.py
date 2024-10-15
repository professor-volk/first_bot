import ast

#очитсть БД
def user_dp_clear():
    open('database.txt', 'w').close()

#считать БД
def user_db_get() -> str:
    with open('database.txt') as f:
        s = ast.literal_eval(f.readline())
        return s

#обновить БД
def user_db_upload(dict):
    with open('database.txt', 'w') as f:
        f.write(str(dict))
        print(dict)





