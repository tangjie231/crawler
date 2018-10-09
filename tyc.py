import httputils as http
from tyc_crawler import TycCrawler
from tyc_db import DbUtil
import tyc_parse as parse

if __name__ == '__main__':
    headers_str = '''
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7
Cache-Control: max-age=0
Connection: keep-alive
Cookie: TYCID=c3df0590c3ff11e8a6731f588b6cb697; undefined=c3df0590c3ff11e8a6731f588b6cb697; ssuid=9828544322; _ga=GA1.2.1004909863.1538236393; aliyungf_tc=AQAAAHvsACLD5wMArCl4atke7Cqmfpn5; csrfToken=_cFtc3NU0EqTxPDp9UHKoQkX; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1538412241,1538412252,1538480234,1539010963; _gid=GA1.2.2122337562.1539010963; _gat_gtag_UA_123487620_1=1; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzOTAxMDY0MywiZXhwIjoxNTU0NTYyNjQzfQ.amCP_rFpT_TAGT1V_OG6VAdKeqnEWng5fqSMrcMdLkLL9-9_8Vqc_tpo6Oy4hx6FwaZ_5lWj51a1AaG4Nqmy3w%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25229%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218514236025%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzOTAxMDY0MywiZXhwIjoxNTU0NTYyNjQzfQ.amCP_rFpT_TAGT1V_OG6VAdKeqnEWng5fqSMrcMdLkLL9-9_8Vqc_tpo6Oy4hx6FwaZ_5lWj51a1AaG4Nqmy3w; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1539010986
Host: www.tianyancha.com
Referer: https://www.tianyancha.com/search?key=%e7%be%8e%e5%9b%a2%e7%82%b9%e8%af%84
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
    '''

    headers = http.parse_header(headers_str)
    req_url = 'https://www.tianyancha.com/search'

    company_file_prefix = '/Users/tangjie/Downloads/companies/'
    company_detail_file_prefix = '/Users/tangjie/Downloads/companies/details/'

    tyc_parse = TycCrawler(headers, req_url, company_file_prefix, company_detail_file_prefix)

    dbUtil = DbUtil()
    conn, cursor = dbUtil.get_conn_and_cursor()
    company_list = dbUtil.query_all_not_deal_company(cursor)

    for company_tuple in company_list:
        company = {
            'company_name': company_tuple[2],
            'user_id': company_tuple[0],
            'company_code': '',
            'legal_name': '',
            'reg_capital': ''
        }
        user_id = company['user_id']
        city_name = company_tuple[1]

        company_name = company['company_name']
        if company['company_name'].find(city_name) == -1:
            company_name = city_name + company['company_name']

        params = {
            'key': company_name
        }

        if tyc_parse.do_crawler(_user_id=user_id, _params=params) is None:
            dbUtil.close_cursor_conn(cursor, conn)
            break
        else:
            main_file_path = company_file_prefix + user_id + '.html'
            parse.parse_company(main_file_path, company)

            detail_file_path = company_detail_file_prefix + user_id + '.html'
            parse.parse_company_detail(detail_file_path, company)

            dbUtil.modify_company_info(company, cursor)
            print('处理完成：', company['company_name'])
