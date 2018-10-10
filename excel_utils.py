import xlrd
import xlwt
from tyc_db import DbUtil


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
    dbUtil = DbUtil()
    conn, cursor = dbUtil.get_conn_and_cursor()

    company_tuple_list = dbUtil.query_all_company(cursor)
    company_list = []
    dbUtil.close_cursor_conn(cursor, conn)

    for company_tuple in company_tuple_list:
        company_list.append({
            'user_id': company_tuple[0],
            'city_name': company_tuple[1],
            'org_company_name': company_tuple[2],
            'company_code': company_tuple[3],
            'legal_name': company_tuple[4],
            'reg_capital': company_tuple[5],
        })

    write_to_excel_file('e:/rs.xlsx', company_list)
