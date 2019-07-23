from upload import *

if __name__ == '__main__':
    try:
        init()
        # print('=====init md5 finished=====')
        up1_report()
        print('=======web 1 finished======')
        # up2_report()
        # print('=======web 2 finished======')
        # up3_report()
        # print('=======web 3 finished======')
        # up4_report()
        # print('=======web 4 finished======')
        # up8_report()
        # print('=======web 8 finished======')
        # up10_report()
        # print('=======web 10 finished======')
        close_driver()

    except KeyboardInterrupt:
        sig_int_handler()
