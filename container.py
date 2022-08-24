import os
import dotenv
import time
import sched
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from event import get_events_list

URL = 'https://gms.myreefer.com/ProActtransport/Logon'


def get_web_driver() -> webdriver:
    root_dir = os.path.dirname(__file__)
    driver_path = os.path.join(root_dir, 'chromedriver.exe')
    service = Service(driver_path)
    application_webdriver = webdriver.Chrome(service=service)
    return application_webdriver


def fill_sign_in_field(input_driver: webdriver, field: str, send_keys: str):
    input_field = input_driver.find_element(By.XPATH, f"//input[@placeholder='{field}']")
    input_field.click()
    input_field.send_keys(send_keys)


def sign_in(sign_in_driver: webdriver):
    root_dir = os.path.dirname(__file__)
    dotenv_path = os.path.join(root_dir, '.env')
    dotenv_file = dotenv.find_dotenv(dotenv_path)
    dotenv.load_dotenv(dotenv_file)
    login = os.environ.get('LOGIN')
    password = os.environ.get('PASSWORD')
    fill_sign_in_field(sign_in_driver, 'Username', login)
    fill_sign_in_field(sign_in_driver, 'Password', password)
    sign_in_button = sign_in_driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
    sign_in_button.click()
    time.sleep(3)


def set_temperature(container: str, temperature: str):
    driver = get_web_driver()
    driver.get(URL)
    driver.maximize_window()
    sign_in(driver)
    time.sleep(2)
    driver.find_element(By.XPATH, f"//*[contains(text(), '{container}')]").click()
    driver.find_element(By.CSS_SELECTOR, 'div.k-icon.k-collapse-prev').click()
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Commands').click()

    time.sleep(2)
    executes = driver.find_elements(By.CSS_SELECTOR, "a.k-grid-executeCommand.k-button")
    executes[2].click()
    time.sleep(2)
    temperature_input_field = driver.find_element(By.XPATH, "//input[@placeholder='Set point']")
    temperature_input_field.send_keys(temperature)

    # driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary').click()
    time.sleep(60)


def create_and_run_event_schedule(events: list):
    s = sched.scheduler(time.time, time.sleep)
    for event in events:
        kwargs = {'container': event.container, 'temperature': event.temperature}
        s.enterabs(event.time, 0, set_temperature, kwargs=kwargs)
    s.run()


def run_program():
    events_list = get_events_list()
    create_and_run_event_schedule(events_list)


if __name__ == '__main__':
    run_program()
