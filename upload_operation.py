from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
from config import *
from operations import *
import csv
import os
import glob
import time
import re


def report_form(num: int, md5: str) -> str:
    if num == 1:
        return 'http://www.ijiami.cn/apply/safeDetail?appId=' + md5
    elif num == 2:
        return webs[num] + 'app/' + md5 + '/report/'
    elif num == 3:
        return 'https://service.security.tencent.com/uploadimg_dir/jingang/' + md5 + '.html'


def up2(file_path) -> str:
    result_url = 'null'
    open_web_auto_refresh(driver, webs[2])
    time.sleep(1)
    driver.find_element_by_name("file").send_keys(os.path.abspath(file_path))
    time.sleep(2)
    for i in range(0, 3):
        try:
            result_url = str(driver.find_element_by_class_name("click-to-open").get_attribute('textContent'))
            break
        except NoSuchElementException:
            time.sleep(2)
            continue

    return result_url


def up3(file_path) -> bool:
    result = False
    driver.get("https://service.security.tencent.com/kingkong")
    time.sleep(0.5)
    try:
        driver.find_element_by_id("txtFile").send_keys(os.path.abspath(file_path))
        driver.implicitly_wait(100)
        result = True
    except NoSuchElementException:
        pass
    return result


def up4(file_path) -> bool:
    driver.get("https://habo.qq.com/")
    driver.implicitly_wait(30)
    driver.find_element_by_id("file_upload2").send_keys(os.path.abspath(file_path))
    while driver.current_url == webs[4]:
        try:
            if re.search('display: block',
                         driver.find_element_by_id('User_upgrade').get_attribute('style')) is not None:
                return False
        except Exception as e:
            print(e)

        time.sleep(2)
    return True


def dict_to_md5_csv(tmp: dict):
    result = []
    for app in tmp:
        result.append({'app': app, 'md5': tmp[app]})
    return result


def dict_to_report_csv(tmp: dict):
    result = []
    for app in tmp:
        result.append({'app': app, 'report': tmp[app]})
    return result


def read_md5(csv_path) -> dict:
    with open(csv_path, newline='') as csv_file:
        result = dict({})
        for row in csv.DictReader(csv_file):
            result[row['app']] = row['md5']
    return result


def up2_report():
    report_header = ['app', 'report']
    report_csv_path = os.path.join(reports_path, 'report_2.csv')
    with open(report_csv_path, "w", encoding='utf8', newline='') as out_report:
        report_writer = csv.DictWriter(out_report, report_header)

        report_writer.writeheader()
        md5_data = read_md5(md5_csv_path)
        for app in md5_data.keys():
            if md5_data[app] != 'fails':
                report_writer.writerow(
                    {'app': app, 'report': report_form(2, md5_data[app])})


def init():
    global md5_csv_path, options, driver

    try_to_mkdir(md5_path)
    try_to_mkdir(reports_path)
    try_to_mkdir(APKs_path)
    try_to_mkdir(reports_path)

    if md5_clear_flag:
        print('All the data in md5 file will be cleared')
    if omit_fail_file:
        print('Failed files will be omitted')

    md5_header = ['app', 'md5']

    md5_csv_path = os.path.join(md5_path, 'md5.csv')

    options = webdriver.ChromeOptions()
    if head_less_flag:
        print('all the web will be hidden')
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    if use_users_cache:
        print('use users\' data to speed up')
        options.add_argument(
            "--user-data-dir=" + user_profile)
    try:
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
    except InvalidArgumentException:
        print('please kill chrome completely')
        sys.exit(1)
    driver.set_page_load_timeout(10)

    is_exist = os.path.exists(md5_csv_path)
    pre_data = {}
    if is_exist and (not md5_clear_flag):
        pre_data = read_md5(md5_csv_path)

    with open(md5_csv_path, "w", encoding='utf8', newline='') as out_md5:
        md5_writer = csv.DictWriter(out_md5, md5_header)
        md5_writer.writeheader()
        md5_writer.writerows(dict_to_md5_csv(pre_data))

        if not omit_fail_file:
            for app in list(pre_data.keys()):
                if pre_data[app] == 'fails':
                    pre_data.pop(app)
            md5_writer.writerows(dict_to_md5_csv(pre_data))

        for file_path in glob.glob(os.path.join(APKs_path, '*.apk')):
            base_name = os.path.basename(file_path)
            if base_name not in pre_data.keys():
                print(base_name + ' ...', end=' ')
                result_url = up2(file_path)
                if result_url != 'null':
                    md5 = result_url.split('/')[4]
                    md5_writer.writerow({'app': base_name, 'md5': md5})
                    print('ok')
                else:
                    md5_writer.writerow({'app': base_name, 'md5': 'fails'})
                    print('fails')


def update_report(num: int, data: dict):
    report_csv_path = os.path.join(reports_path, 'report_' + str(num) + '.csv')
    report_data = read_report(report_csv_path)
    report_header = ['app', 'report']
    with open(report_csv_path, "w", encoding='utf8', newline='') as out_report:
        report_writer = csv.DictWriter(out_report, report_header)
        report_writer.writeheader()
        rows = dict_to_report_csv(report_data)
        report_writer.writerows(rows)
        for app in data.keys():
            if data[app] != 'fails' and app not in report_data.keys():
                report_writer.writerow(
                    {'app': app, 'report': report_form(num, data[app])})


def up3_report():
    md5_data = read_md5(md5_csv_path)
    report_csv_path = os.path.join(reports_path, 'report_' + str(3) + '.csv')

    report_data = read_report(report_csv_path)
    report_header = ['app', 'report']
    with open(report_csv_path, "w", encoding='utf8', newline='') as out_report:
        report_writer = csv.DictWriter(out_report, report_header)
        report_writer.writeheader()
        report_writer.writerows(dict_to_report_csv(report_data))

        for file_path in glob.glob(os.path.join(APKs_path, '*.apk')):
            base_name = os.path.basename(file_path)
            if base_name in report_data.keys():
                continue
            print(base_name + ' ...')
            if up3(file_path):
                print('uploading')
                while driver.find_element_by_id('apk_label').get_attribute('textContent') == '正在上传':
                    time.sleep(2)

                if driver.find_element_by_id('apk_label').get_attribute('textContent') == '上传文件不合法':
                    print('file is illegal')
                    continue
                report_writer.writerow(
                    {'app': base_name, 'report': report_form(3, md5_data[base_name])})

                print('ok')
            else:
                md5_data[base_name] = 'fails'
                print('fails')


def read_report(csv_path: str) -> dict:
    with open(csv_path, newline='') as csv_file:
        result = dict({})
        for row in csv.DictReader(csv_file):
            result[row['app']] = row['report']
    return result


def up4_report():
    report_csv_path = os.path.join(reports_path, 'report_4.csv')
    report_data = {}
    if os.path.exists(report_csv_path):
        report_data = read_report(report_csv_path)
    report_header = ['app', 'report']
    with open(report_csv_path, "w", encoding='utf8', newline='') as out_report:

        report_writer = csv.DictWriter(out_report, report_header)
        report_writer.writeheader()
        report_writer.writerows(dict_to_report_csv(report_data))

        open_web_auto_refresh(driver, webs[4])
        for i in range(0, 10):
            try:
                driver.find_element_by_id("file_upload-button").click()
                break
            except TimeoutException:
                continue

        while driver.find_element_by_id('loginframe').get_attribute('style') != '':
            time.sleep(3)

        for file_path in glob.glob(os.path.join(APKs_path, '*.apk')):
            base_name = os.path.basename(file_path)
            if base_name in report_data.keys():
                continue

            print(base_name + ' ...', end=' ')
            if os.path.getsize(file_path) > 30000000:
                print('too big')
            elif up4(file_path):

                print('ok')
                report_writer.writerow({'app': base_name, 'report': driver.current_url})
            else:
                print('fails')
                break


def up8(file_path) -> bool:
    driver.get(webs[8])
    driver.find_element_by_id("fileinput").send_keys(os.path.abspath(file_path))
    time.sleep(1)
    driver.find_element_by_id("btnStartID").click()
    for i in range(0, 5):
        if driver.current_url == webs[8]:
            time.sleep(2)
        else:
            return True
    return False


def up8_report():
    global driver
    driver.quit()
    report8_path = os.path.join(reports_path, 'report_8')
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.set_page_load_timeout(10)

    try_to_mkdir(report8_path)

    pre_reports = set({})

    for file_path in glob.glob(os.path.join(report8_path, '*.png')):
        pre_reports.add(os.path.basename(file_path).split('.png')[0])

    for file_path in glob.glob(os.path.join(APKs_path, '*.apk')):

        base_name = os.path.basename(file_path)
        print(base_name + ' ...')

        if base_name.split('.apk')[0] in pre_reports:
            continue

        if os.path.getsize(file_path) > 7000000:
            print('file too big')
            continue

        if up8(file_path):
            while True:
                try:
                    if driver.find_element_by_class_name('nocomments').get_attribute('style') == 'display: block;':
                        break
                    else:
                        continue
                except NoSuchElementException:
                    time.sleep(4)
            if webshot(os.path.join(report8_path, base_name.split('.apk')[0])):
                print('ok')
            else:
                print('screen shot is too big')
        else:
            print('fails')


def up10(file_path) -> bool:
    driver.get(webs[10])
    driver.find_element_by_id("file-input").send_keys(os.path.abspath(file_path))
    time.sleep(3)
    return True


def up10_report():
    global driver
    driver.quit()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.set_page_load_timeout(10)

    report10_path = os.path.join(reports_path, 'report_10')

    try_to_mkdir(report10_path)

    pre_reports = set({})

    for file_path in glob.glob(os.path.join(report10_path, '*.png')):
        pre_reports.add(os.path.basename(file_path).split('.png')[0])

    for file_path in glob.glob(os.path.join(APKs_path, '*.apk')):
        base_name = os.path.basename(file_path)
        if base_name.split('.apk')[0] in pre_reports:
            continue

        print(base_name + ' ...', end=' ')
        if up10(file_path):
            if webshot(os.path.join(report10_path, base_name.split('.apk')[0])):
                print('ok')
            else:
                print('too big')
        else:
            print('fails')


def webshot(pic_path) -> bool:
    driver.maximize_window()
    # 返回网页的高度的js代码
    js_height = "return document.body.clientHeight"
    try:
        k = 1
        height = driver.execute_script(js_height)
        if height > 30000:
            return False
        while True:
            if k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 500)
                print(js_move)
                driver.execute_script(js_move)
                time.sleep(0.2)
                height = driver.execute_script(js_height)
                k += 1
            else:
                break
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(pic_path + ".png")
        print("Process {} get one pic !!!".format(os.getpid()))
        time.sleep(0.1)
        return True
    except Exception as e:
        print(pic_path, e)
        return False


def up1(file_path):
    driver.get(webs[1])
    time.sleep(3)
    try:
        driver.find_element_by_class_name('up ').click()
        while driver.current_url == webs[1]:
            time.sleep(1)
        print(driver.current_url)
        inputs = driver.find_elements_by_tag_name('input')
        file_input = inputs[0]
        for i in inputs:
            content = i.get_attribute('id')
            if re.match('html*', content) is not None:
                file_input = i
                break
        file_input.send_keys(os.path.abspath(file_path))
        print('uploading')
        while driver.find_element_by_class_name('uploadProgress').get_attribute(
                'style') != 'height: 10px; display: none;':
            time.sleep(2)
        driver.find_element_by_id('sub').click()
        while driver.current_url != webs[1]:
            time.sleep(1)

    except NoSuchElementException:
        return False

    return True


def upload_files_1():
    global driver

    report_csv_path = os.path.join(reports_path, '_tmp_1_records_.csv')
    report_data = dict({})
    if os.path.exists(report_csv_path):
        report_data = read_report(report_csv_path)
    report_header = ['app', 'report']
    with open(report_csv_path, "w", encoding='utf8', newline='') as out_report:
        report_writer = csv.DictWriter(out_report, report_header)
        report_writer.writeheader()
        report_writer.writerows(dict_to_report_csv(report_data))
        open_web_auto_refresh(driver, 'http://www.ijiami.cn/tlogin')
        driver.find_element_by_id('email').clear()
        time.sleep(1)
        driver.find_element_by_id('email').send_keys('n1803749f@e.ntu.edu.sg')
        driver.find_element_by_id('pwd').send_keys('1234qwer')
        while driver.current_url == 'http://www.ijiami.cn/tlogin':
            time.sleep(2)

        for file_path in glob.glob(os.path.join(APKs_path, '*.apk')):
            base_name = os.path.basename(file_path)
            if base_name in report_data.keys():
                continue

            print(base_name + ' ...')
            if up1(file_path):
                report_writer.writerow(
                    {'app': base_name, 'report': 'http://www.ijiami.cn/apply/Detect'})
                print('ok')
            else:
                print('fails')


def up1_report():
    global driver
    upload_files_1()
    report_header = ['app', 'report']
    open_web_auto_refresh(driver, webs[1])
    time.sleep(2)
    report_csv_path = os.path.join(reports_path, 'report_1.csv')

    with open(report_csv_path, "w", encoding='utf8', newline='') as out_report:
        report_writer = csv.DictWriter(out_report, report_header)
        report_writer.writeheader()
        cards = driver.find_elements_by_class_name('card')
        for card in cards[1:]:
            name = card.find_element_by_xpath('.//div[@class="name"]').get_attribute('textContent')
            title = card.find_element_by_xpath('./div[@class="titles"]').get_attribute('app')
            link = report_form(1, title)
            report_writer.writerow({'app': name, 'report': link})


def close_driver():
    driver.quit()
