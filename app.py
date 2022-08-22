import os
import dotenv
from datetime import datetime
from csv import DictReader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

URL = 'https://gms.myreefer.com/ProActtransport/Logon'
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class Event:
    def __init__(self, schedule_row):
        self.container = schedule_row['container']
        self.time = datetime.strptime(schedule_row['datetime'], "%d/%m/%y %H:%M")
        self.temperature = schedule_row['temperature']


def get_schedule():
    file = [el for el in os.listdir() if '.csv' in el].pop()
    open_file = open(file, 'r')
    reader = DictReader(open_file)
    schedule = [Event(row) for row in reader]
    return schedule


def get_web_driver() -> webdriver:
    base_dir = os.path.dirname(__file__)
    driver_path = os.path.join(base_dir, 'chromedriver.exe')
    service = Service(driver_path)
    application_webdriver = webdriver.Chrome(service=service)
    return application_webdriver


def fill_sign_in_field(input_driver: webdriver, field: str, send_keys: str):
    input_field = input_driver.find_element(By.XPATH, f"//input[@placeholder='{field}']")
    input_field.click()
    input_field.send_keys(send_keys)


def sign_in(sign_in_driver: webdriver):
    login = os.environ.get('LOGIN')
    password = os.environ.get('PASSWORD')
    fill_sign_in_field(sign_in_driver, 'Username', login)
    fill_sign_in_field(sign_in_driver, 'Password', password)
    sign_in_button = sign_in_driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
    sign_in_button.click()
    time.sleep(10)


def set_temperature_on_container(container: str, temperature: str, setting_driver):
    container_button = setting_driver.find_element(By.XPATH, f"//*[contains(text(), '{container}')]")
    container_button.click()
    menu_expand = setting_driver.find_element(By.CSS_SELECTOR, 'div.k-icon.k-collapse-prev')
    menu_expand.click()

    commands_button = setting_driver.find_element(By.PARTIAL_LINK_TEXT, 'Commands')
    commands_button.click()

    time.sleep(3)
    executes = setting_driver.find_elements(By.CSS_SELECTOR, "a.k-grid-executeCommand.k-button")

    change_temp_execute = executes[2]
    change_temp_execute.click()

    temperature_input_field = setting_driver.find_element(By.XPATH, "//input[@placeholder='Set point']")
    temperature_input_field.send_keys(temperature)

    execute_button = setting_driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
    execute_button.click()


def run_program():
    plan = get_schedule()
    click_contaner = plan[0].container
    temperature_to_set = plan[0].temperature

    print(click_contaner)
    driver = get_web_driver()
    driver.get(URL)
    driver.maximize_window()
    sign_in(driver)

    set_temperature_on_container(
        container=click_contaner,
        temperature=temperature_to_set,
        setting_driver=driver)


if __name__ == '__main__':

    run_program()
