from multiprocessing import Pool
from app.main import BaseClub
from app.get_data import read_users


def do_login(user):
    base = BaseClub()
    base.login_dublicat(user.get('username'), user.get('pass'))
    

if __name__ == '__main__':
    p = Pool(1)
    p.map(do_login, read_users('users.txt'))
