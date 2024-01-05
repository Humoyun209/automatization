from multiprocessing import Pool

from send_message.main import SendMessage
from app.get_data import read_users


def func(user):
    sm = SendMessage()
    sm.to_chat(
        user.get('username'),
        poluchateli=['ProgreSS'],
        title="Let's gooo",
        description="Let's go Sean"
    )
    sm.auto_answer("Работаю...")


if __name__ == '__main__':
    p = Pool(1)
    p.map(func, read_users('users.txt'))