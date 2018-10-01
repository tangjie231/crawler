import httputils as http
import excelutils as execel
import time
from lxml import etree
import os
import requests

headers_str = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7
Connection: keep-alive
Cookie: aliyungf_tc=AQAAAOSB4V3GagcArCl4aqV6TjyLdnfB; csrfToken=nXU701agfxE5AG-f9Z0ETXfo; TYCID=c3df0590c3ff11e8a6731f588b6cb697; undefined=c3df0590c3ff11e8a6731f588b6cb697; ssuid=9828544322; _ga=GA1.2.1004909863.1538236393; RTYCID=c0ce2958d97744e5814217edec6b8645; CT_TYCID=260ef70d3f954ccc91385315b16f4e17; _gid=GA1.2.595447162.1538366380; cloud_token=ccbd5f944410495fac41b7dc255627a3; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1538236392,1538366380,1538368191; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzODM2ODIwNCwiZXhwIjoxNTUzOTIwMjA0fQ.Eg8Nqq9BPivtoUjudqO3whChNi84vbTUHQEb0Uu9FI94W6ubFL9d2UzuITLCsp3_dtNnk91RpR6oUXh9HwCyog%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25222%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218514236025%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzODM2ODIwNCwiZXhwIjoxNTUzOTIwMjA0fQ.Eg8Nqq9BPivtoUjudqO3whChNi84vbTUHQEb0Uu9FI94W6ubFL9d2UzuITLCsp3_dtNnk91RpR6oUXh9HwCyog; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1538368224
Host: www.tianyancha.com
Referer: https://antirobot.tianyancha.com/captcha/verify?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fsearch%3Fkey%3D%25e7%25be%258e%25e5%259b%25a2%25e7%2582%25b9%25e8%25af%2584&rnd=
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36
'''

headers, cookies = http.parse_header_and_cookie(headers_str)

req_url = 'https://www.tianyancha.com/search'

company_list = execel.read_excel(r'/Users/tangjie/Downloads/第二次撞库数据.xlsx')
company_file_prefix = '/Users/tangjie/Downloads/companies/'
company_detail_file_prefix = '/Users/tangjie/Downloads/companies/details/'

for company in company_list:
    company_name = company['company_name']
    user_id = company['user_id']

    params = {
        'key': company_name
    }

    if not os.path.exists(company_file_prefix + user_id + '.html'):
        reqs = http.get_req(req_url, params=params, headers=headers, cookies=cookies)
        if reqs.status_code != requests.codes.ok:
            break

        html = etree.HTML(reqs.text)
        rs = html.xpath('//div[@class="login_page position-rel"]')
        if len(rs) > 0:
            break

        with open(company_file_prefix + user_id + '.html', 'w', encoding='utf-8', errors="ignore") as f:
            text = reqs.text
            f.writelines(text)
            print('处理完成：', company_file_prefix + user_id + '.html')
            time.sleep(0.2)

            # 处理统一代号
            html = etree.HTML(text)
            rs = html.xpath('//a[@tyc-event-ch="CompanySearch.Company"]')
            if len(rs) > 0:
                href_ = rs[0].attrib['href']
                print('详细信息链接:', href_)

                if not os.path.exists(company_detail_file_prefix + user_id + '.html'):
                    reqs = http.get_req(href_, headers=headers, cookies=cookies)
                    if reqs.status_code != requests.codes.ok:
                        break

                    html = etree.HTML(reqs.text)
                    rs = html.xpath('//div[@class="login_page position-rel"]')
                    if len(rs) > 0:
                        break

                    text = reqs.text
                    detail_f = open(company_detail_file_prefix + user_id + '.html', mode='w', encoding='utf-8', errors="ignore")
                    detail_f.writelines(text)
                    detail_f.flush()
                    detail_f.close()
                    print('处理完成：', company_detail_file_prefix + user_id + '.html')
                    time.sleep(0.2)

    else:
        with open(company_file_prefix + user_id + '.html', 'r', encoding='utf-8', errors="ignore") as f:
            try:
                html = etree.HTML(f.read())
                rs = html.xpath('//a[@tyc-event-ch="CompanySearch.Company"]')
                if len(rs) > 0:
                    href_ = rs[0].attrib['href']
                    if not os.path.exists(company_detail_file_prefix + user_id + '.html'):
                        reqs = http.get_req(href_, headers=headers, cookies=cookies)
                        if reqs.status_code != requests.codes.ok:
                            break

                        html = etree.HTML(reqs.text)
                        rs = html.xpath('//div[@class="login_page position-rel"]')
                        if len(rs) > 0:
                            break

                        text = reqs.text
                        detail_f = open(company_detail_file_prefix + user_id + '.html', mode='w', encoding='utf-8', errors="ignore")
                        detail_f.writelines(text)
                        detail_f.flush()
                        detail_f.close()
                        print('处理完成：', company_detail_file_prefix + user_id + '.html')

                        time.sleep(0.2)
            except Exception as e:
                print(e)
