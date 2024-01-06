import pickle
import time
from fake_useragent import UserAgent
from selenium import  webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Pool
from app.globals import *


class BaseClub:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={UserAgent().random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(
            options=options,
            service=Service('app/chromedriver')
        )
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def delete_cloudfare(self):
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array
                                         delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON
                                         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object
                                         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise
                                         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy
                                         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol"""
            },
        )

    def login_dublicat(self, username, password):
        try:
            self.driver.get(LOGIN_URL)
            self.driver.find_element(By.XPATH, LOGIN_USERNAME_INPUT).send_keys(
                username
            )
            self.driver.find_element(By.XPATH, LOGIN_PASSWORD_INPUT).send_keys(
                password
            )
            self.driver.find_element(By.XPATH, LOGIN_BTN).click()
            time.sleep(1)
            with open(f"caches/{username}", "wb") as f:
                pickle.dump(self.driver.get_cookies(), f)
            time.sleep(10)
        except Exception as e:
            print(type(e))
        finally:
            self.driver.close()
            self.driver.quit()

    def load_cookies(self, username):
        with open(f"caches/{username}", "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            time.sleep(1)
            self.driver.refresh()
            time.sleep(1)
