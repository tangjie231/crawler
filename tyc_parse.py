import os
from lxml import etree


def parse_company(file_path, company_info):
    if os.path.exists(file_path):
        try:
            tree = etree.HTML(open(file_path, encoding='utf-8', mode='r').read())

            rs = tree.xpath('//a[@tyc-event-ch="CompanySearch.Company"]')
            if len(rs) > 0:
                company_info['detail_url'] = rs[0].attrib['href']

            rs = tree.xpath('//a[@class="legalPersonName hover_underline"]')
            if len(rs) > 0:
                company_info['legal_name'] = rs[0].text

            rs = tree.xpath('//div[contains(text(),"注册资本")]/child::span')
            if len(rs) > 0:
                company_info['reg_capital'] = rs[0].text

        except Exception as e:
            print('ERROR:', file_path)
            print("error: {0}".format(e))


def parse_company_detail(file_path, company_info):
    if os.path.exists(file_path):
        try:
            tree = etree.HTML(open(file_path, encoding='utf-8', mode='r').read())

            rs = tree.xpath('//td[contains(text(),"统一信用代码")]/following-sibling::td[1]')
            if len(rs) > 0:
                company_info['company_code'] = rs[0].text
        except Exception as e:
            print('ERROR:', file_path)
            print("error: {0}".format(e))