from upload import *


if __name__ == '__main__':

    try:
        init()
        print('=====init md5 finished=====')
        update_report_1()
        # up1_report()
        # print('=======web 1 finished======')
        # up2_report()
        # print('=======web 2 finished======')
        # up3_report()
        # print('=======web 3 finished======')
        # up4_report()
        # print('=======web 4 finished======')
        # up_bangbang_report()
        # print('===web bang bang finished==')
        # up9_report()
        print('=======web 9 finished======')
        # up8_report()
        # print('=======web 8 finished======')
        # up10_report()
        # print('=======web 10 finished======')
    except KeyboardInterrupt:
        sig_int_handler()
    finally:
        close_driver()
