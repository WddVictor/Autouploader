# README

### 开发环境

macOS Mojave 10.14.5

Python 3.6



### 环境搭建

Selenium运行库

```shell
pip install selenium
```

或者

```shell
pip3 install selenium
```



Chrom driver 下载

1. 使用chrome打开[chrome://version/](chrome://version/) 查看chrome版本

2. 下载相应driver [版本对照表](https://blog.csdn.net/BinGISer/article/details/88559532)

3. 前往[官网](http://chromedriver.chromium.org/downloads)或[镜像](http://npm.taobao.org/mirrors/chromedriver/)下载

4. config.py中配置chromedriver路径

   

### 配置文件（config.py）

|      名称       | 值                                                    |
| :-------------: | ----------------------------------------------------- |
|   driver_path   | chrome 的驱动路径                                     |
|    APKs_path    | 存放apk                                               |
|  reports_path   | 存放报告                                              |
|    md5_path     | 存放md5.csv                                           |
|                 |                                                       |
| md5_clear_flag  | 是否重新生成md5                                       |
| omit_fail_file  | 是否忽略未查询到md5的文件                             |
| head_less_flag  | 是否在运行过程中显示浏览器（8号和10号网站一定不显示） |
| use_users_cache | 是否使用用户缓存                                      |
|                 |                                                       |
|      webs       | 访问的网站地址                                        |



### 常见问题

可以在main.py中注释掉相应的代码来只访问某几个网站 e.g. # up10_report()
