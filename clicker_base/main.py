import time
from app.main import BaseClub
from clicker_base.variables import *
from selenium.webdriver.common.by import By


class Clicker(BaseClub):
    def __init__(self) -> None:
        super().__init__()

    def fill_form(self, username, otvetchik, summa, ssilka_otvetchik, telegram, description):
        i = 1
        try:
            while True:
                try:
                    self.driver.get(ADD_ARBITRAJ_URL)
                    time.sleep(1)
                    if i == 1:
                        self.load_cookies(username)
                    defendant = self.driver.find_element(By.XPATH, DEFENDANT)
                    self.driver.execute_script(
                        "return arguments[0].scrollIntoView(true)", defendant
                    )
                    defendant.send_keys(otvetchik)
                    self.driver.find_element(By.XPATH, PRICE).send_keys(summa)
                    self.driver.find_element(By.XPATH, GARANT_RADIO).click()
                    self.driver.find_element(By.XPATH, ANSWER_DEFANDANT).send_keys(
                        ssilka_otvetchik
                    )
                    telegram_input = self.driver.find_element(By.XPATH, ANSWER_TELEGRAM)
                    self.driver.execute_script(
                        "return arguments[0].scrollIntoView(true)", telegram_input
                    )
                    telegram_input.send_keys(telegram)
                    self.driver.find_element(By.XPATH, DESCRIPTION).send_keys(description)
                    self.driver.find_element(By.XPATH, SEND_BTN).click()
                    i += 1
                    time.sleep(5)
                except Exception as e:
                    print(type(e))
        except Exception as e:
            self.driver.quit()
            exit()