import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.main import BaseClub
from register_base.variables import *


class ZnMail(BaseClub):
    def __init__(self) -> None:
        super().__init__()
        self.sleep_time = 10

    def register_user(self, username, email, password):
        try:
            self.driver.get("https://dublikat.club/register/")
            self.delete_cloudfare()
            self.driver.find_element(By.XPATH, REGISTER_EMAIL_INPUT).send_keys(email)
            self.driver.find_element(By.XPATH, REGISTER_USERNAME_INPUT).send_keys(
                username
            )
            self.driver.find_element(By.XPATH, REGISTER_PASSWORD_INPUT).send_keys(
                password
            )
            checkbox = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, REGISTER_CHECKBOX_INPUT))
            )
            checkbox.click()

            time.sleep(0.5)

            submit = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, REGISTER_SUBMIT_BTN))
            )
            submit.click()

            buy_btn = self.driver.find_element(By.XPATH, BUY_BUTTON)
            self.delete_cloudfare()

            self.driver.execute_script(
                "return arguments[0].scrollIntoView(true)", buy_btn
            )

            buy_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, BUY_BUTTON))
            )
            buy_btn.click()

            time.sleep(self.sleep_time)
        except Exception as e:
            print(type(e))

    def do_login_zn_email(self, email: str, password: str):
        try:
            self.driver.get("https://firstmail.ltd/webmail/login")
            input_email = WebDriverWait(self.driver, 3000).until(
                EC.presence_of_element_located((By.XPATH, ZN_EMAIL_INPUT))
            )
            input_email.send_keys(email)
            self.driver.find_element(By.XPATH, ZN_EMAIL_PASSWORD).send_keys(password)
            self.driver.find_element(By.XPATH, ZN_SUBMIT).click()
            confirm_msg = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, MESSAGE_CONFIRM))
            )
            confirm_msg.click()

            WebDriverWait(self.driver, 30).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, MESSAGE_IFRAME))
            )
            self.driver.find_element(By.XPATH, EMAIL_CONFIRM_BTN).click()
            time.sleep(0.5)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(0.2)
            self.driver.refresh()
            time.sleep(5)
            with open("users.txt", "a") as f:
                f.write(f"{email}:{password}\n")
            time.sleep(0.5)
        except Exception as e:
            print(type(e))
