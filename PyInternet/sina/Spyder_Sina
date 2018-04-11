import requests
from bs4 import BeautifulSoup
import os
import time
from selenium.webdriver.chrome.options import Options
import selenium.webdriver as webdriver
import datetime
import PyInternet.sina.Database_manager as dbManager


_author_ = 'Oltremare_D'


class FetchAtContent(object):
    """
    头部信息，均截取自网页请求头部信息中
    """
    User_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    Accept_encoding = 'gzip,deflate,br'
    Accept_language = 'zh-CN,zh;q=0.9'

    # 时间转化标准
    Trans_standard = '%Y-%m-%d %H:%M:%S'
    # 默认cookie过期时间
    Expire_date = 5
    # 装载需要存储的内容
    content_list = []

    def __init__(self, user_name, user_password):
        self.user_name = user_name
        self.user_password = user_password
        self.now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db = dbManager.DatabaseManager.init_database()
        self.cursor = self.db.cursor()
        self.cookie = ''

    def is_expire(self):
        # 查询cookie更新时间
        query_sql = 'select FETCH_COOKIE_DATE from log where USER_NAME="{}"'.format(self.user_name)
        self.cursor.execute(query_sql)

        # 获取查询结果
        result = self.cursor.fetchall()

        # 判断是否是新添加账号或者cookie已经过期并返回结果
        return False if len(result) and self._cal_day_delta(result) < self.Expire_date else True

    def _cal_day_delta(self, result):
        pre_date = result[0][0]
        delta = (datetime.datetime.strptime(self.now_date, self.Trans_standard)
                 - datetime.datetime.strptime(pre_date, self.Trans_standard)).days
        return delta

    # 获取At页的数据
    def fetch_content(self, page_num):
        query_cookie_sql = 'select COOKIE from log where USER_NAME="{}"'.format(self.user_name)
        self.cursor.execute(query_cookie_sql)
        result = self.cursor.fetchall()
        self.cookie = result[0][0]
        if self.is_expire():
            self.fetch_login_cookie_code()

        # 头部信息
        head = {'Accept': self.Accept,
                'Accept-Encoding': self.Accept_encoding,
                'Accept-Language': self.Accept_language,
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Cookie': self.cookie,
                'Host': 'weibo.cn',
                'Pragma': 'no-cache',
                'Referer': 'https://weibo.cn/',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': self.User_agent
                }
        # 设置访问的页数
        data = dict()
        data["page"] = page_num
        # 使用session的形式不会造成超过30次的重定向错误
        s = requests.session()
        s.headers['User-Agent'] = self.User_agent
        # 进入@我页面
        at_page = s.post("https://weibo.cn/at/comment", headers=head, data=data)
        at_page.encoding = 'utf-8'
        # 解析得到有at页的总页数
        soup = BeautifulSoup(at_page.text, 'lxml')
        find_list = soup.find_all('input', attrs={"name": "mp"})
        total_page = find_list[0]["value"]
        if at_page.ok:
            return int(total_page), at_page.text
        else:
            return 0, ''

    def update_at_content(self, at_page):
        if len(at_page) is 0:
            print('获取at页内容为空，更新失败')
            return ''

        # 解析Html中的div，查找条件为class=c 获取到微博的内容
        soup = BeautifulSoup(at_page, 'lxml')
        items = soup.find_all('div', class_='c')
        # 因为网页头部有3个不是评论的div、网页尾部有2两个不是评论的div，故去除
        for item in items[3:len(items)-2]:
            item_text = item.text
            print(item_text)
            # 将类似于“...评论[40]--大戴丶:@大戴丶丶  03月02日 08:49 回复他”的无效内容剔除
            self.content_list.append(item_text[: item_text.find('...')]+'\n')

    def fetch_login_cookie_code(self):
        # 配置Headless版本、无GUI的Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        # 启动浏览器
        chrome_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
        os.environ['webdriver.chrome.driver'] = chrome_driver
        driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
        driver.get(
            'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F')
        # 设置等待加载的时间 3秒
        time.sleep(3)

        # 根据标签id定位填入微博账号、密码并登录
        driver.find_element_by_id('loginName').send_keys(self.user_name)
        driver.find_element_by_id('loginPassword').send_keys(self.user_password)
        driver.find_element_by_id('loginAction').click()

        # 预留时间让页面跳转，跳转到首页获取到的cookie才是正确的
        time.sleep(5)

        # 获取cookies
        cookies = driver.get_cookies()
        cookie_list = []
        for cookie in cookies:
            key = cookie['name']
            value = cookie['value']
            cookie_list.append(key+"="+value)
        self.cookie = ';'.join(cookie_list)
        self._save_cookie(self.cookie)

    def _save_cookie(self, cookie):
        # 这里使用了mysql中的语法
        # 判断该条记录是否存在，若存在就更新，不存在则插入记录
        save_sql = 'insert into log(FETCH_COOKIE_DATE, USER_NAME, COOKIE) values ("{}", "{}", "{}") ' \
                   'on duplicate key update FETCH_COOKIE_DATE="{}", COOKIE="{}"'.format(self.now_date, self.user_name,
                                                                                        cookie, self.now_date, cookie)
        print(save_sql)
        self.cursor.execute(save_sql)
        self.db.commit()

    def save_content(self):
        with open("C:\\Users\Administrator\Desktop\weibo_at_record.txt", 'wt', encoding="utf-8") as file:
            for item in self.content_list:
                file.write(item)
        file.close()
        print('更新成功')

    def close(self):
        dbManager.DatabaseManager.close(self.cursor, self.db)


if __name__ == '__main__':
    fetcher = FetchAtContent('输入用户名', '输入密码')
    # 获取at页html
    pages, html = fetcher.fetch_content(1)
    # 执行更新操作
    fetcher.update_at_content(html)
    if pages > 1:
        for page in range(1, pages+1):
            _, html = fetcher.fetch_content(page)
            # 执行更新操作
            fetcher.update_at_content(html)
    fetcher.save_content()
    # 关闭数据库
    fetcher.close()
