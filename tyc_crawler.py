from lxml import etree
import os
import requests


class TycCrawler:
    def __init__(self, _headers, _main_page_url, _company_file_prefix, _detail_file_prefix):
        self.headers = _headers
        self.main_page_url = _main_page_url
        self.company_file_prefix = _company_file_prefix
        self.detail_file_prefix = _detail_file_prefix
        self.session = None

    """

    def __init_redis_client(self):
        sentinel = Sentinel([('sentinel1.redist.djdns.cn', 28100), ('sentinel1.redist.djdns.cn', 28101),
                             ('sentinel1.redist.djdns.cn', 28102)], socket_timeout=0.5)


        return sentinel.master_for('my18200master', socket_timeout=0.5, decode_responses=True)


    def __save_last_deal_company(self, company_id):
        self.redis_client.set("crawler_last_company", company_id)

    def __get_last_deal_company(self):
        return self.redis_client.get("crawler_last_company")
    """

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
            # time.sleep(3)

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
            # time.sleep(5)
            return "go_on"
