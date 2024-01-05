from app.get_data import read_users
from register_base.main import ZnMail
from multiprocessing import Pool


def func(user):
    zn = ZnMail()
    zn.register_user(user.get("username"), user.get("email"), user.get("pass"))
    zn.do_login_zn_email(user.get("email"), user.get("pass"))


if __name__ == "__main__":
    p = Pool(1)
    p.map(func, read_users('emails.txt'))
