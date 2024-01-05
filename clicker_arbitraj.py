from multiprocessing import Pool
from app.get_data import read_users
from clicker_base.main import Clicker


def do_fill_form(user):
    cl = Clicker()
    cl.fill_form(
        username=user.get('username'),

        # Изменение только внизу
        otvetchik="progreSS",
        summa=200,
        ssilka_otvetchik="https://t.me/humoyun209",
        telegram="https://t.me/humoyun209",
        description=f"About me",
    )
    

if __name__ == '__main__':
    p = Pool(1)
    p.map(do_fill_form, read_users('users.txt'))