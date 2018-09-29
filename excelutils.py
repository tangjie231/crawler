import xlrd
import json

def read_excel():
    excel_file = xlrd.open_workbook(r'd:\第二次撞库数据.xlsx')
    sheet = excel_file.sheet_by_index(0)
    for row in sheet.get_rows():
        print(row[2].value)

# read_excel()

json_str = '{"data":[{"id":27063827,"name":"<em>北京盛诺基医药科技有限</em>公司","type":1,"matchType":"公司名称匹配"},{"id":2343082190,"name":"青岛珅奥<em>基</em>生物工程<em>有限</em>公司","type":1,"matchType":"股东信息匹配"},{"id":27063722,"name":"<em>北京</em>恒<em>诺基医药科技有限</em>公司","type":1,"matchType":"股东信息匹配"},{"id":2310780535,"name":"武汉友芝友生物制<em>药有限</em>公司","type":1,"matchType":"股东信息匹配"},{"id":27854067,"name":"<em>北京</em>欣<em>诺基医药科技有限</em>公司","type":1,"matchType":"股东信息匹配"}],"state":"ok"}'
rs = json.loads(json_str)
print(rs['data'][0]['id'])
