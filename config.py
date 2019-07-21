driver_path = "./driver/chromedriver"
user_profile = '/Users/victor/Library/Application Support/Google/Chrome/Default'

reports_path = './report'
md5_path = './md5'
APKs_path = "./APKs"

md5_clear_flag = False  # clear md5.csv and re-fill
omit_fail_file = True   # omit the failed files (in md5.csv)
head_less_flag = False  # display the chrome during execution
use_users_cache = True  # use cache to speed up web redirection

webs = ['', 'http://www.ijiami.cn/apply/Detect',
        'http://appscan.360.cn/',
        'https://service.security.tencent.com/kingkong',
        'https://habo.qq.com/',
        'http://www.nagain.com/appscan/',
        'http://sanddroid.xjtu.edu.cn/#home',
        'https://www.nowsecure.com/solutions/mobile-app-vetting/',
        'https://undroid.av-comparatives.org/index.php',
        'https://apkscan.nviso.be/',
        'https://www.sisik.eu/apk-tool',
        'https://appcritique.boozallen.com/'
        ]
