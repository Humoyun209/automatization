from multiprocessing import Pool

from send_message.main import SendMessage
from app.get_data import read_users


def func(users):
    sm = SendMessage()
    sm.do_work(
        users,
        poluchateli=["ProgreSS"],
        title="Let's gooo",
        description="Let's go Sean",
        message="Работаю...",
    )


if __name__ == '__main__':
    kolichestvo_potokov = 1
    p = Pool(kolichestvo_potokov)
    p.map(func, [read_users('users.txt') for _ in range(kolichestvo_potokov)])