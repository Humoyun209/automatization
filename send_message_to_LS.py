from multiprocessing import Pool

from app.generator_users import split_users
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
    group_users = split_users(
        read_users('users.txt'),
        spliter=2
    )
    kolichestvo_potokov = len(group_users)
    p = Pool(kolichestvo_potokov)
    p.map(func, group_users)