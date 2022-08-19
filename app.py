import os
import dotenv
from datetime import datetime
from csv import DictReader
from selenium import webdriver
from selenium.webdriver.common.by import By

CHROME_WEBDRIVER_PATH = 'chromedriver.exe'
URL = 'https://gms.myreefer.com/ProActtransport/Logon'
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


def get_schedule():
    file = [el for el in os.listdir() if '.csv' in el].pop()
    open_file = open(file, 'r')
    reader = DictReader(open_file)
    for row in reader:
        time = datetime.strptime(row['hour'], "%d/%m/%y %H:%M")
        print(row['container'], time, row['temperature'])


def get_web_driver() -> webdriver:
    application_webdriver = webdriver.Chrome(CHROME_WEBDRIVER_PATH)
    return application_webdriver


def fill_input_field(input_driver: webdriver, field: str, send_keys: str):
    input_field = input_driver.find_element(By.XPATH, f"//input[@placeholder='{field}']")
    input_field.click()
    input_field.send_keys(send_keys)


def sign_in(sign_in_driver: webdriver):
    login = os.environ.get('LOGIN')
    password = os.environ.get('PASSWORD')
    fill_input_field(sign_in_driver, 'Username', login)
    fill_input_field(sign_in_driver, 'Password', password)
    sign_in_button = sign_in_driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
    sign_in_button.click()


def run_program():
    driver = get_web_driver()
    driver.get(URL)
    sign_in(driver)


if __name__ == '__main__':
    get_schedule()
