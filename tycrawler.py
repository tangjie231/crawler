import httputils as http
import excelutils as execel
import time
from lxml import etree
import os
import requests
import redis
from redis.sentinel import Sentinel


class TycPaser:
    def __init__(self, _headers, _main_page_url, _company_file_prefix, _detail_file_prefix):
        self.headers = _headers
        self.main_page_url = _main_page_url
        self.company_file_prefix = _company_file_prefix
        self.detail_file_prefix = _detail_file_prefix
        self.session = None
        self.redis_client = self.__init_redis_client()
        self.last_deal_company_id = self.__get_last_deal_company()
        self.deal_first = False

    def __init_redis_client(self):
        sentinel = Sentinel([('sentinel1.redist.djdns.cn', 28100), ('sentinel1.redist.djdns.cn', 28101),
                             ('sentinel1.redist.djdns.cn', 28102)], socket_timeout=0.5)

        return sentinel.master_for('my18200master', socket_timeout=0.5, decode_responses=True)

    def __save_last_deal_company(self, company_id):
        self.redis_client.set("crawler_last_company", company_id)

    def __get_last_deal_company(self):
        return self.redis_client.get("crawler_last_company")

    def do_crawler(self, _user_id, _params):
        return self.__get_and_parser_mian_page(_user_id, _params)

    def __get_session(self):
        if self.session is None:
            self.session = requests.session()
            self.session.headers = self.headers
            return self.session
        else:
            return self.session

    def __get_and_parser_mian_page(self, user_id, params):
        if self.last_deal_company_id is not None and self.deal_first is False:
            if user_id != self.last_deal_company_id:
                return "go_on"
            else:
                self.deal_first = True

        # 保存要处理的公司（用户id）
        self.__save_last_deal_company(user_id)

        main_html_file = self.company_file_prefix + user_id + '.html'
        if os.path.exists(main_html_file):
            with open(main_html_file, 'r', encoding='utf-8', errors="ignore") as f:
                return self.__get_and_parse_detail_page(user_id, f.read())

        req_url = self.main_page_url
        session = self.__get_session()

        response = session.get(req_url, params=params)
        if response.status_code != requests.codes.ok:
            print("主页返回code：", response.status_code)
            return None

        html = etree.HTML(response.text)
        rs = html.xpath('//div[@class="login_page position-rel"]')
        if len(rs) > 0:
            print("主页返回登录页")
            return None

        # 写入main_page文件
        with open(main_html_file, 'w', encoding='utf-8', errors="ignore") as f:
            text = response.text
            f.writelines(text)
            print('处理完成：', main_html_file)
            #time.sleep(3)

            # 写入detial文件
            return self.__get_and_parse_detail_page(user_id, text)

    def __get_and_parse_detail_page(self, user_id, html_content):
        html = etree.HTML(html_content)
        rs = html.xpath('//a[@tyc-event-ch="CompanySearch.Company"]')
        if len(rs) == 0:
            return "go_on"

        detail_href = rs[0].attrib['href']
        print('详细信息链接:', detail_href)

        detail_file = self.detail_file_prefix + user_id + '.html'
        if os.path.exists(detail_file):
            return "go_on"

        session = self.__get_session()
        response = session.get(detail_href)

        if response.status_code != requests.codes.ok:
            print("详情页返回code：", response.status_code)
            return None

        html = etree.HTML(response.text)
        rs = html.xpath('//div[@class="login_page position-rel"]')
        if len(rs) > 0:
            print("详情页返回到登录页面")
            return None

        with open(detail_file, mode='w', encoding='utf-8', errors="ignore") as f:
            text = response.text
            f.writelines(text)
            print('处理完成：', detail_file)
            #time.sleep(5)
            return "go_on"


if __name__ == '__main__':
    headers_str = '''
   Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Cookie: TYCID=128660e0c2f611e8ab81759e05b6e185; undefined=128660e0c2f611e8ab81759e05b6e185; ssuid=2060762260; _ga=GA1.2.1376999845.1538122277; aliyungf_tc=AQAAACCBq3HyJgQAorfGb+83T6OItinz; csrfToken=NymNPgZ3DifLRl5q514QG3SY; bannerFlag=true; cloud_token=1a9acb94aac94718abc00071cfeb47fb; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1538204181,1538208021,1538272537,1538964189; _gid=GA1.2.338539365.1538964190; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzODk2MzkxOSwiZXhwIjoxNTU0NTE1OTE5fQ.DlP_oG0v47B2sqhgsoCe4Uj_B0W4780zIDnWVL01JLjNlhFEAzgqS8EjJNG0DX2jhZJcI-JPWNzerJ62JvkAyA%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25229%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218514236025%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzODk2MzkxOSwiZXhwIjoxNTU0NTE1OTE5fQ.DlP_oG0v47B2sqhgsoCe4Uj_B0W4780zIDnWVL01JLjNlhFEAzgqS8EjJNG0DX2jhZJcI-JPWNzerJ62JvkAyA; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1538964268; _gat_gtag_UA_123487620_1=1
Host: www.tianyancha.com
Pragma: no-cache
Referer: https://www.tianyancha.com/search?key=%e7%be%8e%e5%9b%a2%e7%82%b9%e8%af%84&rnd=
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36
    '''

    headers = http.parse_header(headers_str)

    req_url = 'https://www.tianyancha.com/search'

    company_list = execel.read_excel(r'd:/第二次撞库数据.xlsx')
    company_file_prefix = 'e:/companies/'
    company_detail_file_prefix = 'e:/companies/details/'

    tyc_parse = TycPaser(headers, req_url, company_file_prefix, company_detail_file_prefix)

    for company in company_list:
        company_name = company['company_name']
        user_id = company['user_id']

        params = {
            'key': company_name
        }

        if tyc_parse.do_crawler(_user_id=user_id, _params=params) is None:
            break
