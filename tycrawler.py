import httputils as http
import excelutils as execel
import time
from lxml import etree
import os

headers_str = '''
Host: www.tianyancha.com
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: https://www.tianyancha.com/company/2313012135?rnd=
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: TYCID=128660e0c2f611e8ab81759e05b6e185; undefined=128660e0c2f611e8ab81759e05b6e185; ssuid=2060762260; _ga=GA1.2.1376999845.1538122277; _gid=GA1.2.1651814957.1538122277; aliyungf_tc=AQAAACCBq3HyJgQAorfGb+83T6OItinz; csrfToken=NymNPgZ3DifLRl5q514QG3SY; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1538123520,1538204181,1538208021,1538272537; cloud_token=46547d7df95e4edd8bd761be335295fb; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzODI5NzYwMywiZXhwIjoxNTUzODQ5NjAzfQ.pWVmuddNfFvOKsoOoLkbF8kZlPWS88WwbqLbxxSL7N7-EYKz-e5uYm-3bPswW9yteMUnkE422mvR10S6s3TSuQ%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25221%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218514236025%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzODI5NzYwMywiZXhwIjoxNTUzODQ5NjAzfQ.pWVmuddNfFvOKsoOoLkbF8kZlPWS88WwbqLbxxSL7N7-EYKz-e5uYm-3bPswW9yteMUnkE422mvR10S6s3TSuQ; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1538301365; _gat_gtag_UA_123487620_1=1
'''

headers,cookies = http.parse_header_and_cookie(headers_str)

req_url = 'https://www.tianyancha.com/search'

company_list = execel.read_excel(r'd:\test_company.xlsx')
company_file_prefix = 'E:/companies/'
company_detail_file_prefix = 'E:/companies/details/'

for company in company_list:
    company_name = company['company_name']
    user_id = company['user_id']

    params = {
        'key': company_name
    }

    if not os.path.exists(company_file_prefix+user_id+'.html'):
        reqs = http.get_req(req_url, params=params, headers=headers, cookies=cookies)
        with open(company_file_prefix+user_id+'.html','w',encoding='utf-8') as f:
            text = reqs.text
            f.writelines(text)
            print('处理完成：',company_file_prefix+user_id+'.html')

            #处理统一代号
            html = etree.HTML(text)
            rs = html.xpath('//a[@tyc-event-ch="CompanySearch.Company"]')
            if len(rs) > 0:
                href_ = rs[0].attrib['href']
                print('详细信息链接:', href_)

                if not os.path.exists(company_detail_file_prefix + user_id + '.html'):
                    reqs = http.get_req(href_, headers=headers, cookies=cookies)
                    text = reqs.text
                    detail_f = open(company_detail_file_prefix + user_id + '.html', mode='w', encoding='utf-8')
                    detail_f.writelines(text)
                    detail_f.flush()
                    detail_f.close()
                    print('处理完成：', company_detail_file_prefix + user_id + '.html')

        time.sleep(0.2)
    else:
        with open(company_file_prefix + user_id + '.html', 'r', encoding='utf-8') as f:
            try:
                html = etree.HTML(f.read())
                rs = html.xpath('//a[@tyc-event-ch="CompanySearch.Company"]')
                if len(rs) > 0:
                    href_ = rs[0].attrib['href']
                    if not os.path.exists(company_detail_file_prefix + user_id + '.html'):
                        reqs = http.get_req(href_, headers=headers, cookies=cookies)
                        text = reqs.text
                        detail_f = open(company_detail_file_prefix + user_id + '.html', mode='w', encoding='utf-8')
                        detail_f.writelines(text)
                        detail_f.flush()
                        detail_f.close()
                        print('处理完成：', company_detail_file_prefix + user_id + '.html')
                        time.sleep(0.2)
            except Exception as e:
                print(e)









