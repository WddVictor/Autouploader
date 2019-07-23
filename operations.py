from selenium.common.exceptions import TimeoutException
import os
import sys
from config import *
import csv


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


def report_form(num: int, md5: str) -> str:
    if num == 1:
        return 'http://www.ijiami.cn/apply/safeDetail?appId=' + md5
    elif num == 2:
        return webs[num] + 'app/' + md5 + '/report/'
    elif num == 3:
        return 'https://service.security.tencent.com/uploadimg_dir/jingang/' + md5 + '.html'


def dict_to_csv(tmp: dict, key1: str, key2: str) -> list:
    result = []
    for app in tmp:
        result.append({key1: app, key2: tmp[app]})
    return result


def read_md5(csv_path, md5_2_app: bool = False) -> dict:
    with open(csv_path, encoding='utf8', newline='') as csv_file:
        result = dict({})
        for row in csv.DictReader(csv_file):
            if md5_2_app:
                result[row['md5']] = row['app']
            else:
                result[row['app']] = row['md5']
    return result


def read_report(csv_path: str, read_by_name: bool = False) -> dict:
    result = dict({})
    try:
        with open(csv_path, encoding='utf8', newline='') as csv_file:
            for row in csv.DictReader(csv_file):
                if read_by_name:
                    result[row['name']] = row['md5']
                    result[row['md5']] = row['name']
                else:
                    result[row['app']] = row['report']
    except FileNotFoundError:
        pass
    return result


def report_csv_path(num: int) -> str:
    return os.path.join(reports_path, 'report_' + str(num) + '.csv')
