from selenium.common.exceptions import TimeoutException
import os
import sys


def open_web_auto_refresh(driver, web: str):
    while True:
        try:
            driver.get(web)
            break
        except TimeoutException:
            continue


def open_new_tab(driver):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])


def try_to_mkdir(dir_path):
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        print(os.path.basename(dir_path), 'has already existed')


def sig_int_handler():
    print('Forced Exit')
    sys.exit(1)
