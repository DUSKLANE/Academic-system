import datetime
import base64

import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad





class Login:
    def __init__(self, username: str, password: str):
        """
        初始化登录类
        :param username: 用户名
        :param password: 密码
        :param session: 已创建的 requests 会话对象
        """
        self.username = username
        self.password = password
        self.url = 'https://wwebvpn.sdjtu.edu.cn'
        self.croypto = None
        self.execution = None
        self.islogin = False
        self.session = requests.Session()
        self.login()

    def des_encrypt(self, key: str, plaintext: str) -> str:
        """
        使用 DES 算法对密码进行加密(ECB模式)
        :param key: 密钥（从页面中获取的加密密钥）
        :param plaintext: 明文密码
        :return: 返回 Base64 编码后的加密密码
        """
        key = base64.b64decode(key)
        # 创建 AES ECB 模式 cipher
        cipher = AES.new(key, AES.MODE_ECB)
        # PKCS7 填充并加密
        encrypted = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
        return base64.b64encode(encrypted).decode('utf-8')

    def get_login_view_data(self):
        """
        获取登录页面所需的数据(如 'croypto' 和 'execution')
        :return: 包含 'croypto' 和 'execution' 的元组
        """
        try:
            response = self.session.get(self.url)
            self.url = response.url    # 获取重定向后的 URL
            response.raise_for_status()  # 如果返回状态码是4xx或5xx，会抛出异常
        except requests.RequestException as e:
            print(f"获取登录页面失败: {e}")
        
        soup = BeautifulSoup(response.text, 'html.parser')  # 使用 BeautifulSoup 解析 HTML
        self.croypto = soup.find('p', {'id': 'login-croypto'}).contents[0]
        self.execution = soup.find('p', {'id': 'login-page-flowkey'}).contents[0]

    def loginjwxt(self):
        """
        登录教务系统
        """
        res1 = self.session.get(f'https://wwebvpn.sdjtu.edu.cn/http/77726476706e69737468656265737421a1ae13d27666301e2c5ddae2c90377/sso.jsp')
        res2 = self.session.get(f'https://wwebvpn.sdjtu.edu.cn/https/77726476706e69737468656265737421f3f652cd69236c5a6a1dc7a99c406d36e9/cas/login?service=http%3A%2F%2F192.168.253.164%2Fsso.jsp') 

    def login(self) -> bool:
        """
        执行登录操作，使用用户名和密码进行登录
        :return: 登录成功返回 True, 失败返回 False
        """
        # 获取登录页面需要的数据
        self.get_login_view_data()

        if not self.croypto or not self.execution:
            print("未能成功获取登录所需的数据。")
            return False
        
        # 使用 DES 算法加密密码
        encrypted_password = self.des_encrypt(self.croypto, self.password)
        # 准备登录请求的表单数据
        form_data = {
            "username": self.username,
            "type": "UsernamePassword",
            "_eventId": "submit",
            "geolocation": "",
            "execution": self.execution,
            "croypto": self.croypto,
            "password": encrypted_password,
            "captcha_code": "",
        }
        try:
            # 发送登录请求
            result = self.session.post(self.url, data=form_data)
            result.raise_for_status()  # 如果返回状态码是4xx或5xx，会抛出异常
        except requests.RequestException as e:
            print(f"登录请求出错: {e}")
            return False
        
        # 判断登录结果（401 未授权表示登录失败）
        if result.status_code == 401:
            print("登录失败：无效的用户名或密码。")
            return False
        self.loginjwxt()
        print("登录成功。")
        self.islogin = True
        return True
    


def getAllScore(session):
    """
    获取所有课程成绩
    :param session: 已创建的 requests 会话对象
    :return: 包含所有课程成绩的列表
    """
    data = {
        'kksj': '',
        'kcxz': '',
        'kcmc': '',
        'xsfs': 'all',
    }
    response = session.post(
        'https://wwebvpn.sdjtu.edu.cn/https/77726476706e69737468656265737421eaff4b8b203c26437a029db9d65027203034e6/jsxsd/kscj/cjcx_list',
        data=data,
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'dataList'})
    scores = []
    rows = table.find_all('tr')
    for row in rows[1:]:  # 跳过表头
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        scores.append(cols)
    return scores


def getWeekTimetable(session, date = ''):
    """
    获取课表
    :param session: 已创建的 requests 会话对象
    :param datetime: 查询的日期,如果为空则查询当周的课表
    :return: 包含课表信息的列表
    """
    if  date == '':
        date = datetime.date.today()
    data = {
        'rq': date,
        }
    response = session.post(
        'https://wwebvpn.sdjtu.edu.cn/https/77726476706e69737468656265737421eaff4b8b203c26437a029db9d65027203034e6/jsxsd/framework/main_index_loadkb.jsp?vpn-12-o2-zhjwgl.sdjtu.edu.cn',
        data=data,
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    timetable = []
    rows = table.find_all('tr')
    for row in rows[1:]:  # 跳过表头
        col = []
        for i in row.find_all('td')[1:]:# 跳过第一列
            p_tag = i.find('p')
            if p_tag and 'title' in p_tag.attrs:
                course_info_list = p_tag['title'].split('<br/>')
                course_info = course_info_list[2].split('：')[1] + '@' + course_info_list[4].split('：')[1]
            else:
                course_info = ''
            col.append(course_info)
        timetable.append(col)
    return timetable

def getAllTimetable(session):
    """
    获取学期理论课程的课表
    :param session: 已创建的 requests 会话对象
    :return: 课程的课表信息
    """
    response = requests.get('https://wwebvpn.sdjtu.edu.cn/https/77726476706e69737468656265737421eaff4b8b203c26437a029db9d65027203034e6/jsxsd/xskb/xskb_list.do')
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'kbtable'})
    
    

if __name__ == '__main__':
    # login = Login('', '')
    # print(login.islogin)
    # score_data = getAllScore(login.session)  # 传入 session
    # print(score_data)
    # print(json.dumps(getWeekTimetable(login.session, ''), ensure_ascii=False))
    # print(getAllScore(login.session))
    pass