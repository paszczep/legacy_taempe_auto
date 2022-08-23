import os
import dotenv
from datetime import datetime
from csv import DictReader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import sched

URL = 'https://gms.myreefer.com/ProActtransport/Logon'
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class Event:
    def __init__(self, plan_row):
        self.container = plan_row['container']
        self.time = time.mktime(datetime.strptime(plan_row['datetime'], "%d/%m/%Y %H:%M").timetuple())
        self.temperature = plan_row['temperature']


def get_events_list() -> list:
    file = [el for el in os.listdir() if '.csv' in el].pop()
    open_file = open(file, 'r')
    reader = DictReader(open_file)
    schedule = [Event(row) for row in reader]
    for event in schedule:
        print(event.time, event.container, f'{event.temperature} °C', sep='\t')
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
    time.sleep(3)


def set_temperature(container: str, temperature: str):
    driver = get_web_driver()
    driver.get(URL)
    driver.maximize_window()
    sign_in(driver)

    driver.find_element(By.XPATH, f"//*[contains(text(), '{container}')]").click()
    driver.find_element(By.CSS_SELECTOR, 'div.k-icon.k-collapse-prev').click()
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Commands').click()

    time.sleep(3)
    executes = driver.find_elements(By.CSS_SELECTOR, "a.k-grid-executeCommand.k-button")

    change_temp_execute = executes[2]
    change_temp_execute.click()
    time.sleep(2)
    temperature_input_field = driver.find_element(By.XPATH, "//input[@placeholder='Set point']")
    temperature_input_field.send_keys(temperature)

    execute_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
    execute_button.click()


def create_event_schedule(events: list):
    s = sched.scheduler(time.time, time.sleep)
    for event in events:
        kwargs = {'container': event.container, 'temperature': event.temperature}
        s.enterabs(event.time, 0, set_temperature, kwargs=kwargs)
    s.run()


def run_program():
    events_list = get_events_list()
    create_event_schedule(events_list)


if __name__ == '__main__':
    run_program()
