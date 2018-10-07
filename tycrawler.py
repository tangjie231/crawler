import httputils as http
import excelutils as execel
import time
from lxml import etree
import os
import requests


class TycPaser:
    def __init__(self, _headers, _main_page_url, _company_file_prefix, _detail_file_prefix):
        self.headers = _headers
        self.main_page_url = _main_page_url
        self.company_file_prefix = _company_file_prefix
        self.detail_file_prefix = _detail_file_prefix
        self.session = None

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
            time.sleep(0.2)

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
            time.sleep(0.2)
            return "go_on"


if __name__ == '__main__':
    headers_str = '''
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7
Connection: keep-alive
Cookie: TYCID=c3df0590c3ff11e8a6731f588b6cb697; undefined=c3df0590c3ff11e8a6731f588b6cb697; ssuid=9828544322; _ga=GA1.2.1004909863.1538236393; _gid=GA1.2.595447162.1538366380; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzODM2ODIwNCwiZXhwIjoxNTUzOTIwMjA0fQ.Eg8Nqq9BPivtoUjudqO3whChNi84vbTUHQEb0Uu9FI94W6ubFL9d2UzuITLCsp3_dtNnk91RpR6oUXh9HwCyog%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25222%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218514236025%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzODM2ODIwNCwiZXhwIjoxNTUzOTIwMjA0fQ.Eg8Nqq9BPivtoUjudqO3whChNi84vbTUHQEb0Uu9FI94W6ubFL9d2UzuITLCsp3_dtNnk91RpR6oUXh9HwCyog; aliyungf_tc=AQAAAHvsACLD5wMArCl4atke7Cqmfpn5; csrfToken=_cFtc3NU0EqTxPDp9UHKoQkX; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1538368191,1538412241,1538412252,1538480234; _gat_gtag_UA_123487620_1=1; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1538480256
Host: www.tianyancha.com
Referer: https://www.tianyancha.com/search?key=%e7%be%8e%e5%9b%a2%e7%82%b9%e8%af%84&rnd=
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
    '''

    headers = http.parse_header(headers_str)

    req_url = 'https://www.tianyancha.com/search'

    company_list = execel.read_excel(r'/Users/tangjie/Downloads/第二次撞库数据.xlsx')
    company_file_prefix = '/Users/tangjie/Downloads/companies/'
    company_detail_file_prefix = '/Users/tangjie/Downloads/companies/details/'

    tyc_parse = TycPaser(headers, req_url, company_file_prefix, company_detail_file_prefix)

    for company in company_list:
        company_name = company['company_name']
        user_id = company['user_id']

        params = {
            'key': company_name
        }

        if tyc_parse.do_crawler(_user_id=user_id, _params=params) is None:
            break
