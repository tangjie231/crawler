import aiohttp
import asyncio
import platform
import httputils as http
import tyc_crawler_async as crawler
from tyc_db import DbUtil


async def do_crawler(dbUtil, cursor):
    headers_str = '''
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9
    Cache-Control: no-cache
    Connection: keep-alive
    Cookie: TYCID=128660e0c2f611e8ab81759e05b6e185; undefined=128660e0c2f611e8ab81759e05b6e185; ssuid=2060762260; _ga=GA1.2.1376999845.1538122277; aliyungf_tc=AQAAACCBq3HyJgQAorfGb+83T6OItinz; csrfToken=NymNPgZ3DifLRl5q514QG3SY; bannerFlag=true; _gid=GA1.2.338539365.1538964190; RTYCID=7637c71bdbf94fcc894f5df188a81a06; CT_TYCID=4567ec9b72b840efa8bf21f8b3679744; cloud_token=685214f76b8c4376b45201295f59ad34; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1538208021,1538272537,1538964189,1539056045; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzOTA1NjI1NCwiZXhwIjoxNTU0NjA4MjU0fQ.gq2JWv3y45f4gz77M1pGg_ndlE1E-_dDV_VuteEGgUov4bEPH-UHVQN5AIjpaJDjD4YFl48qGe-diCMmZ2D1Og%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%252210%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218514236025%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzOTA1NjI1NCwiZXhwIjoxNTU0NjA4MjU0fQ.gq2JWv3y45f4gz77M1pGg_ndlE1E-_dDV_VuteEGgUov4bEPH-UHVQN5AIjpaJDjD4YFl48qGe-diCMmZ2D1Og; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1539056698
    Host: www.tianyancha.com
    Pragma: no-cache
    Referer: https://antirobot.tianyancha.com/captcha/verify?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fsearch%3Fkey%3D%25E7%25BE%258E%25E5%259B%25A2%25E7%2582%25B9%25E8%25AF%2584&rnd=
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36
        '''

    headers = http.parse_header(headers_str)
    req_url = 'https://www.tianyancha.com/search'

    company_file_prefix = '/Users/tangjie/Downloads/companies/'
    company_detail_file_prefix = '/Users/tangjie/Downloads/companies/details/'

    if platform.system() == 'Windows':
        company_file_prefix = 'E:/companies/'
        company_detail_file_prefix = 'E:/companies/details/'

    tyc_crawler = crawler.TycAsyncCrawler(headers, req_url, company_file_prefix, company_detail_file_prefix, dbUtil)

    company_list = dbUtil.query_all_not_main_page_company(cursor)

    tasks = []
    async with aiohttp.ClientSession(headers=headers) as session:
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
            tasks.append(asyncio.ensure_future(tyc_crawler.get_mian_page(session, cursor, user_id, params)))
            await asyncio.gather(*tasks)


    #return await asyncio.wait(tasks)


if __name__ == '__main__':
    dbUtil = DbUtil()
    conn, cursor = dbUtil.get_conn_and_cursor()

    try:
        tasks = []
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(do_crawler(dbUtil, cursor))
        loop.run_until_complete(future)
        loop.close()
    finally:
        dbUtil.close_cursor_conn(cursor, conn)
