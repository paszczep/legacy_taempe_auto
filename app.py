import sys
from container import run_program, get_web_driver
import dotenv
import os
import time


def try_except():
    driver = get_web_driver()
    try:
        run_program(driver)
    except Exception as ex:
        print(f'{ex}')
        time.sleep(15)
        try_except()
    finally:
        driver.close()


def setup():
    root_dir = os.path.dirname(__file__)
    dotenv_path = os.path.join(root_dir, 'env.env')
    dotenv_file = dotenv.find_dotenv(dotenv_path)
    dotenv.load_dotenv(dotenv_file)
    current_login = os.environ['LOGIN']
    login = input(f'login: ') or current_login
    dotenv.set_key(dotenv_file, 'LOGIN', login)

    current_password = os.environ['PASSWORD']
    password = input(f'password: ') or current_password
    dotenv.set_key(dotenv_file, 'PASSWORD', password)


if __name__ == "__main__":

    command_args = sys.argv

    if len(command_args) == 1:
        try_except()
    elif command_args[1] in ('login', 'setup'):
        setup()
    else:
        print('Invalid input')
