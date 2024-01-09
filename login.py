from multiprocessing import Pool
from app.main import BaseClub
from app.get_data import read_users


def do_login(user):
    try:
        base = BaseClub()
        base.login_dublicat(user.get('username'), user.get('pass'))
    except Exception as e:
        print(type(e))
    

if __name__ == '__main__':
    p = Pool(2)
    p.map(do_login, read_users('users.txt'))

print()
