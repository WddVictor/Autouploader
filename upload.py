from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, \
    ElementClickInterceptedException
from operations import *
import csv
import os
import glob
import time
import re


def up1(file_path):
    driver.get(webs[1])
    time.sleep(3)
    try:
        while True:
            try:
                driver.find_element_by_class_name('up ').click()
                break
            except ElementClickInterceptedException:
                continue
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
            if driver.find_element_by_id('cxmcError').get_attribute('textContent') != '':
                raise NoSuchElementException
            time.sleep(1)

    except NoSuchElementException:
        return False

    return True


def upload_files_1():
    report_csv_path_1 = report_csv_path(1)
    report_data = read_report(report_csv_path_1)

    with open(report_csv_path_1, "w", encoding='utf8', newline='') as out_report:
        report_header = ['app', 'report']
        report_writer = csv.DictWriter(out_report, report_header)
        report_writer.writeheader()
        report_writer.writerows(dict_to_csv(report_data, 'app', 'report'))

        for file_path in glob.glob(os.path.join(APKs_path, '*.apk')):
            base_name = os.path.basename(file_path)
            if base_name in report_data.keys():
                if omit_fail_file or (report_data[base_name] != 'tmp' and report_data[base_name] != 'fails'):
                    continue

            print(base_name + ' ...')
            if up1(file_path):
                report_writer.writerow(
                    {'app': base_name, 'report': 'tmp'})
                print('ok')
            else:
                report_writer.writerow(
                    {'app': base_name, 'report': 'fails'})
                print('fails')


def open_web_1():
    open_web_auto_refresh(driver, 'http://www.ijiami.cn/tlogin')
    driver.find_element_by_id('email').clear()
    time.sleep(1)
    driver.find_element_by_id('email').send_keys('N1803749F@e.ntu.edu.sg')
    driver.find_element_by_id('pwd').send_keys('1234qwer')
    driver.find_element_by_id('code').send_keys('')
    wait_web(driver, 'http://www.ijiami.cn/tlogin', False)
    open_web_auto_refresh(driver, webs[1])


def update_report_1():
    name_md5_con = read_report(os.path.join(reports_path, 'name_md5_correspondence.csv'), read_by_name=True)
    report_csv_path_1 = report_csv_path(1)
    report_data = read_report(report_csv_path_1)
    header = ['app', 'report']

    to_write = dict({})
    time.sleep(1)
    cards = driver.find_elements_by_class_name('card')
    cards_data = dict({})
    for card in cards[1:]:
        if card.find_element_by_xpath('./div[@class="titles"]/span').get_attribute('textContent') == '检测中':
            continue
        name = card.find_element_by_xpath('.//div[@class="name"]').get_attribute('textContent')
        if name in name_md5_con.keys():
            continue
        title = card.find_element_by_xpath('./div[@class="titles"]').get_attribute('app')
        link = report_form(1, title)
        cards_data[name] = link

    with open(report_csv_path_1, "w", encoding='utf8', newline='') as out:
        writer = csv.DictWriter(out, header)
        writer.writeheader()
        writer.writerows(dict_to_csv(report_data, 'app', 'report'))
        for name in cards_data.keys():
            link = cards_data[name]
            open_web_auto_refresh(driver, link)
            while True:
                time.sleep(2)
                md5 = driver.find_element_by_id('MD5').get_attribute('textContent')
                if md5 != '':
                    break
            if md5 not in md5_2_app.keys():
                continue
            app = md5_2_app[md5]
            to_write[name] = md5
            writer.writerow({'app': app, 'report': link})

    header = ['name', 'md5']
    with open(os.path.join(reports_path, 'name_md5_correspondence.csv'), "w", encoding='utf8', newline='') as out:
        writer = csv.DictWriter(out, header)
        writer.writeheader()
        writer.writerows(dict_to_csv(name_md5_con, 'name', 'md5'))
        writer.writerows(dict_to_csv(to_write, 'name', 'md5'))


def up1_report():
    open_web_1()
    update_report_1()
    # upload_files_1()


def up2(file_path) -> str:
    open_web_auto_refresh(driver, webs[2])
    time.sleep(1)
    driver.find_element_by_name("file").send_keys(os.path.abspath(file_path))
    time.sleep(2)
    result_url = 'null'

    while True:
        try:
            result_url = str(driver.find_element_by_class_name("click-to-open").get_attribute('textContent'))
            break
        except NoSuchElementException:
            time.sleep(2)
            continue

    return result_url


def up2_report():
    report_header = ['app', 'report']
    report_csv_path_2 = report_csv_path(2)
    with open(report_csv_path_2, "w", encoding='utf8', newline='') as out_report:
        report_writer = csv.DictWriter(out_report, report_header)

        report_writer.writeheader()
        for app in app_2_md5.keys():
            if app_2_md5[app] != 'fails':
                report_writer.writerow(
                    {'app': app, 'report': report_form(2, app_2_md5[app])})


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


def up3_report():
    report_csv_path_3 = report_csv_path(3)

    report_data = read_report(report_csv_path_3)
    if not omit_fail_file:
        report_data = report_filter(report_data, ['fails'])

    report_header = ['app', 'report']
    with open(report_csv_path_3, "w", encoding='utf8', newline='') as out_report:
        report_writer = csv.DictWriter(out_report, report_header)
        report_writer.writeheader()
        report_writer.writerows(dict_to_csv(report_data, 'app', 'report'))

        for file_path in glob.glob(os.path.join(APKs_path, '*.apk')):
            base_name = os.path.basename(file_path)
            if base_name in report_data.keys():
                continue
            print(base_name + ' ...')
            if up3(file_path):
                print('uploading')
                while driver.find_element_by_id('apk_label').get_attribute('textContent') == '正在上传':
                    time.sleep(2)

                if driver.find_element_by_id('apk_label').get_attribute('textContent') not in ('审计完成！', '上传提示'):
                    print('file is illegal')
                    report_writer.writerow(
                        {'app': base_name, 'report': 'fails'})
                    continue
                report_writer.writerow(
                    {'app': base_name, 'report': report_form(3, app_2_md5[base_name])})

                print('ok')
            else:
                report_writer.writerow(
                    {'app': base_name, 'report': 'fails'})
                print('fails')


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


def up4_report():
    report_csv_path_4 = report_csv_path(4)
    report_data = read_report(report_csv_path_4)
    report_header = ['app', 'report']
    with open(report_csv_path_4, "w", encoding='utf8', newline='') as out_report:

        report_writer = csv.DictWriter(out_report, report_header)
        report_writer.writeheader()
        report_writer.writerows(dict_to_csv(report_data, 'app', 'report'))

        open_web_auto_refresh(driver, webs[4])
        for i in range(0, 10):
            try:
                driver.find_element_by_id("file_upload-button").click()
                break
            except TimeoutException:
                time.sleep(3)
                continue

        while driver.find_element_by_id('loginframe').get_attribute('style') != '':
            time.sleep(3)

        for file_path in glob.glob(os.path.join(APKs_path, '*.apk')):
            base_name = os.path.basename(file_path)
            if base_name in report_data.keys():
                continue

            print(base_name + ' ...')
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


def check_files_9() -> list:
    report_data = read_report(report_csv_path(9))
    to_do_files_path = []
    for file_path in glob.glob(os.path.join(APKs_path, '*.apk')):
        base_name = os.path.basename(file_path)
        if base_name in report_data.keys():
            if omit_fail_file or report_data[base_name] != 'fails':
                continue
        else:
            to_do_files_path.append(file_path)
    return to_do_files_path


def up9(file_path: str) -> bool:
    while True:
        a = input()
        if a == 'u':
            return True
        elif a == 'd':
            return False
        else:
            continue

    open_web_auto_refresh(driver, webs[9])
    driver.find_element_by_id('manualFileField').send_keys(os.path.abspath(file_path))
    while True:
        time.sleep(2)
        if driver.find_element_by_id('progressLbl').get_attribute('textContent') == 'Upload completed':
            break
    try:
        driver.find_element_by_link_text('click here')
        return True
    except NoSuchElementException:
        pass
    driver.find_element_by_class_name('g-recaptcha').click()
    time.sleep(2)
    while True:
        try:
            if driver.find_element_by_id('scanButtonContainer').get_attribute(
                    'textContent') == '\n\t\t\tScanning ...\n\t\t':
                time.sleep(2)
                return True
            else:
                driver.find_element_by_id('scanButtonContainer').click()
                time.sleep(3)
        except ElementClickInterceptedException:
            continue


def up9_report():
    to_do_files_path = check_files_9()
    report_data = read_report(report_csv_path(9))
    report_data = report_filter(report_data, ['fails'])
    report_header = ['app', 'report']
    with open(report_csv_path(9), 'w', encoding='utf-8', newline='') as out_report:
        report_writer = csv.DictWriter(out_report, report_header)
        report_writer.writeheader()
        report_writer.writerows(dict_to_csv(report_data, 'app', 'report'))

        for file_path in to_do_files_path:
            base_name = os.path.basename(file_path)
            print(base_name + ' ...')
            if up9(file_path):
                report_writer.writerow({'app': base_name, 'report': report_form(9, app_2_md5[base_name])})
                print('ok')

            else:
                report_writer.writerow({'app': base_name, 'report': 'fails'})
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


def up_bangbang_report():
    open_web_auto_refresh(driver, 'https://dev.bangcle.com/apps/index')
    driver.find_element_by_id('user').clear()
    driver.find_element_by_id('user').send_keys('m1u9d8jq@mail.bccto.me')
    time.sleep(0.5)
    driver.find_element_by_id('psd').send_keys('1234qwer')
    time.sleep(0.5)
    wait_web(driver, webs[12], redirect_to_input_web=True)
    pass


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


def init():
    global md5_csv_path, options, driver, md5_2_app, app_2_md5

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

        if not omit_fail_file:
            for app in list(pre_data.keys()):
                if pre_data[app] == 'fails':
                    pre_data.pop(app)

        md5_writer.writerows(dict_to_csv(pre_data, 'app', 'md5'))

        for file_path in glob.glob(os.path.join(APKs_path, '*.apk')):
            base_name = os.path.basename(file_path)
            if base_name not in pre_data.keys():
                print(base_name + ' ...')
                result_url = up2(file_path)
                if result_url != 'null':
                    md5 = result_url.split('/')[4]
                    md5_writer.writerow({'app': base_name, 'md5': md5})
                    print('ok')
                else:
                    md5_writer.writerow({'app': base_name, 'md5': 'fails'})
                    print('fails')

    app_2_md5 = read_md5(md5_csv_path)
    md5_2_app = read_md5(md5_csv_path, True)

    # report_3_filter()


def report_3_filter():
    report_data = read_report(report_csv_path(3))

    for app in list(report_data.keys()):
        driver.get(report_data[app])
        time.sleep(2)
        try:
            if driver.find_element_by_xpath('/html/head/title').get_attribute(
                    'textContent') == '腾讯安全应急响应中心(TSRC)支持公益事业':
                report_data.pop(app)
        except Exception as e:
            continue
    report_header = ['app', 'report']
    with open(report_csv_path(3), "w", encoding='utf8', newline='') as out_report:
        report_writer = csv.DictWriter(out_report, report_header)
        report_writer.writeheader()
        report_writer.writerows(dict_to_csv(report_data, 'app', 'report'))


def close_driver():
    driver.quit()
