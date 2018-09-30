import xlrd
import xlwt
import os
from lxml import etree


def read_excel(file_name):
    excel_file = xlrd.open_workbook(file_name)
    sheet = excel_file.sheet_by_index(0)

    company_list = []
    is_first_line = True
    for row in sheet.get_rows():
        if is_first_line:
            is_first_line = False
            continue

        user_id = row[0].value
        city_name = row[1].value
        company_name = row[2].value

        org_company_name = company_name
        if company_name.find(city_name) == -1:
            company_name = city_name + company_name

        company_list.append({'user_id': user_id, 'city_name': city_name, 'company_name': company_name,
                             'company_code': '', 'legal_name': '', 'reg_capital': '',
                             'org_company_name': org_company_name})

    return company_list


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

            print('公司信息:', company_info)
        except Exception as e:
            print('ERROR:', file_path)
            print("error: {0}".format(e))


def write_to_excel_file(file_path, company_list):
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("天眼查结果")

    # 写入表格标题
    sheet.write(0, 0, '用户id')
    sheet.write(0, 1, '城市')
    sheet.write(0, 2, '公司主体')
    sheet.write(0, 3, '统一社会信用代码')
    sheet.write(0, 4, '法人')
    sheet.write(0, 5, '注册资本')

    # 写入数据
    curr_row = 1
    for company in company_list:
        sheet.write(curr_row, 0, company['user_id'])
        sheet.write(curr_row, 1, company['city_name'])
        sheet.write(curr_row, 2, company['org_company_name'])
        sheet.write(curr_row, 3, company['company_code'])
        sheet.write(curr_row, 4, company['legal_name'])
        sheet.write(curr_row, 5, company['reg_capital'])
        curr_row = curr_row + 1

    wb.save(file_path)
    print('写入文件', file_path)


if __name__ == '__main__':
    path = 'E:/companies/'
    company_list = read_excel(r'd:\test_company.xlsx')
    for company in company_list:
        file_path = path + company['user_id'] + '.html'
        parse_company(file_path, company)

    write_to_excel_file('d:/rs.xlsx', company_list)
