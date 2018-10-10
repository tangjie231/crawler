from lxml import etree
import os


class TycAsyncCrawler:
    def __init__(self, _headers, _main_page_url, _company_file_prefix, _detail_file_prefix, dbUtil):
        self.headers = _headers
        self.main_page_url = _main_page_url
        self.company_file_prefix = _company_file_prefix
        self.detail_file_prefix = _detail_file_prefix
        self.dbUtil = dbUtil

    async def get_mian_page(self, session, cursor, user_id, params):
        main_html_file = self.company_file_prefix + user_id + '.html'

        if os.path.exists(main_html_file):
            self.dbUtil.modify_company_main_flag(user_id, cursor)
            return

        req_url = self.main_page_url

        async with session.get(req_url, params=params) as resp:
            content = await resp.text()
            if resp.status == 200:
                html = etree.HTML(content)
                rs = html.xpath('//div[@class="login_page position-rel"]')
                if len(rs) > 0:
                    print("主页返回登录页")
                else:
                    with open(main_html_file, 'w', encoding='utf-8', errors="ignore") as f:
                        f.writelines(content)
                        print('处理完成：', main_html_file)
                        self.dbUtil.modify_company_main_flag(user_id, cursor)
            else:
                pass

    async def get_detail_page(self, session,cursor, user_id):
        main_html_file = self.company_file_prefix + user_id + '.html'
        detail_file = self.detail_file_prefix + user_id + '.html'

        if os.path.exists(detail_file):
            self.dbUtil.modify_company_detail_flag(user_id, cursor)
            return

        if os.path.exists(main_html_file):
            with open(main_html_file, 'r', encoding='utf-8', errors="ignore") as f:
                html = etree.HTML(f.read())
                rs = html.xpath('//a[@tyc-event-ch="CompanySearch.Company"]')
                if len(rs) != 0:
                    detail_href = rs[0].attrib['href']
                    print('详细信息链接:', detail_href)

                    async with session.get(detail_href) as resp:
                        content = await resp.text()
                        if resp.status == 200:
                            html = etree.HTML(content)
                            rs = html.xpath('//div[@class="login_page position-rel"]')
                            if len(rs) > 0:
                                print("详情页返回登录页")
                            else:
                                with open(detail_file, mode='w', encoding='utf-8', errors="ignore") as f:
                                    f.writelines(content)
                                    print('处理完成：', detail_file)
                                    self.dbUtil.modify_company_detail_flag(user_id, cursor)
                        else:
                            pass
                else:
                    self.dbUtil.modify_company_detail_flag(user_id, cursor)


if __name__ == '__main__':
    pass
