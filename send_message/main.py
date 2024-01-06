import random
import time

from urllib3.exceptions import MaxRetryError

from app.main import BaseClub
from send_message.variables import *
from selenium.webdriver.common.by import By


class SendMessage(BaseClub):
    def to_chat(self, username, poluchateli: list[str], title, description):
        error = 0
        try:
            self.driver.get('https://dublikat.club')
            self.load_cookies(username)
            lst = ','.join(poluchateli)
            self.driver.get(f"https://dublikat.club/conversations/add?to={lst}")
            title_input = self.driver.find_element(By.XPATH, TITLE_INPUT)
            self.driver.execute_script(
                "return arguments[0].scrollIntoView(true)", title_input
            )
            title_input.send_keys(title)
            self.driver.find_element(By.XPATH, TITLE_DESCRIPTION).send_keys(description)
            self.driver.find_element(By.XPATH, TITLE_SUBMIT_BTN).click()
            time.sleep(random.randint(3, 5))
        except Exception as e:
            error = 1
            print(type(e))
        return error

    def auto_answer(self, message: str):
        try:
            answer_description = self.driver.find_element(By.XPATH, ANSWER_DESCRIPTION)
            self.driver.execute_script("return arguments[0].scrollIntoView(true)", answer_description)
            answer_description.send_keys(message)
            self.driver.find_element(By.XPATH, ANSWER_BTN).click()
            time.sleep(1)
        except Exception as e:
            print(type(e))

    def do_work(self, users: list, poluchateli: list, title, description, message):
        try:
            while True:
                users = [user for user in users if user]
                for i, user in enumerate(users):
                    error = self.to_chat(user.get('username'), poluchateli, title, description)
                    if error == 1:
                        users[i] = None
                    else:
                        self.auto_answer(message)
                    time.sleep(1)
                    self.driver.delete_all_cookies()
                time.sleep(20)
        except Exception:
            self.driver.quit()
            exit()
