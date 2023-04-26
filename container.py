import os
import dotenv
import time
import sched
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from event import get_events_list

URL = 'https://gms.myreefer.com/ProActtransport/Logon'
SLEEP = 2


def get_web_driver() -> webdriver:
    app_webdriver = webdriver.Chrome(ChromeDriverManager().install())
    return app_webdriver


def fill_sign_in_field(input_driver: webdriver, field: str, send_keys: str):
    input_field = input_driver.find_element(By.XPATH, f"//input[@placeholder='{field}']")
    input_field.click()
    input_field.send_keys(send_keys)


def sign_in(sign_in_driver: webdriver):
    root_dir = os.path.dirname(__file__)
    dotenv_path = os.path.join(root_dir, 'env.env')
    dotenv_file = dotenv.find_dotenv(dotenv_path)
    dotenv.load_dotenv(dotenv_file)
    login = os.environ.get('LOGIN')
    password = os.environ.get('PASSWORD')
    fill_sign_in_field(sign_in_driver, 'Username', login)
    fill_sign_in_field(sign_in_driver, 'Password', password)
    sign_in_button = sign_in_driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
    sign_in_button.click()
    time.sleep(SLEEP)


def set_temperature(
        container: str,
        temperature: str,
        # driver: webdriver
):
    driver = get_web_driver()
    driver.get(URL)
    driver.maximize_window()
    sign_in(driver)
    time.sleep(SLEEP)
    driver.find_element(By.XPATH, f"//*[contains(text(), '{container}')]").click()
    driver.find_element(By.CSS_SELECTOR, 'div.k-icon.k-collapse-prev').click()
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Commands').click()

    time.sleep(SLEEP)
    executes = driver.find_elements(By.CSS_SELECTOR, "a.k-grid-executeCommand.k-button")
    executes[2].click()
    time.sleep(SLEEP)
    temperature_input_field = driver.find_element(By.XPATH, "//input[@placeholder='Set point']")
    temperature_input_field.send_keys(temperature)
    driver.implicitly_wait(SLEEP)

    button = driver.find_element(By.ID, 'temperatureSetpointExecuteBtn')
    driver.implicitly_wait(SLEEP)
    # ActionChains(driver).move_to_element(button).click(button).perform()
    time.sleep(SLEEP*15)


def create_and_run_event_schedule(
        events: list,
        # driver: webdriver
):
    s = sched.scheduler(time.time, time.sleep)
    for event in events:
        kwargs = {
            'container': event.container,
            'temperature': event.temperature,
            # 'driver': driver
        }
        s.enterabs(event.time, 0, set_temperature, kwargs=kwargs)
    s.run()


def run_program(
        # driver: webdriver
):
    events_list = get_events_list()
    create_and_run_event_schedule(
        events_list,
        # driver
    )


if __name__ == '__main__':
    for event in get_events_list():
        print(event)
