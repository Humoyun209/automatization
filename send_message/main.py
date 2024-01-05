import random
import time

from urllib3.exceptions import MaxRetryError

from app.main import BaseClub
from send_message.variables import *
from selenium.webdriver.common.by import By


class SendMessage(BaseClub):
    def to_chat(self, username, poluchateli: list[str], title, description):
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
            print(type(e))
            self.driver.quit()

    def auto_answer(self, message: str):
        try:
            while True:
                try:
                    answer_description = self.driver.find_element(By.XPATH, ANSWER_DESCRIPTION)
                    self.driver.execute_script("return arguments[0].scrollIntoView(true)", answer_description)
                    answer_description.send_keys(message)
                    answer_btn = self.driver.find_element(By.XPATH, ANSWER_BTN)
                    self.driver.execute_script("return arguments[0].scrollIntoView(true)", answer_btn)
                    answer_btn.click()
                    time.sleep(10)
                except MaxRetryError as e:
                    self.driver.quit()
                    exit()
                except Exception as e:
                    print(type(e))
        except Exception:
            self.driver.quit()
            exit()
