from urllib import parse
import httputils
#{"mobile":"18514236025","cdpassword":"7f14f2a7d884c450ff0faaf83a0317a0","loginway":"PL","autoLogin":true}
params = {'mobile':'18514236025','cdpassword':'7f14f2a7d884c450ff0faaf83a0317a0','loginway':'PL','autoLogin':True}
'''
params['mobile'] = '18514236025'
params['cdpassword'] = '7f14f2a7d884c450ff0faaf83a0317a0'
params['loginway'] = 'PL'
params['autoLogin'] = True
'''
# https://www.tianyancha.com/
# https://www.tianyancha.com/cd/login.json
req_url = 'https://www.tianyancha.com/wxApi/getJsSdkConfig.json?url=https%3A%2F%2Fwww.tianyancha.com%2F&_=1538213704668'
# json.dumps(params)
params = parse.urlencode(params)
params = bytes(params,'utf-8')
# params = parse.urlencode(params).encode('utf-8')

cookie_obj = httputils.build_new_cookie()

reqs = httputils.get_req(req_url)
#print(resp.read().decode('utf-8'))


req_url = 'https://www.tianyancha.com/search/suggest.json'
cookie_obj = 'ssuid=2060762260; _ga=GA1.2.1376999845.1538122277; _gid=GA1.2.1651814957.1538122277; RTYCID=411aff8a7c7249459e67978cde7adff8; CT_TYCID=981f0ac7eb954f44bd0067ea15816271; csrfToken=NymNPgZ3DifLRl5q514QG3SY; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1538123298,1538123520,1538204181,1538208021; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzODIxODc1NCwiZXhwIjoxNTUzNzcwNzU0fQ.z_MgccDFvdYBJ02Ngw1GSGJOjVg00bCPKQTEiE4ytBcUL-Wp8ey5Jo3dXpjJLL3KMJDr0svoX_0LPmQrnqQAqw%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218514236025%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNDIzNjAyNSIsImlhdCI6MTUzODIxODc1NCwiZXhwIjoxNTUzNzcwNzU0fQ.z_MgccDFvdYBJ02Ngw1GSGJOjVg00bCPKQTEiE4ytBcUL-Wp8ey5Jo3dXpjJLL3KMJDr0svoX_0LPmQrnqQAqw; cloud_token=08ae8f867d8b4c62b41b02a4f39766aa; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1538224121; _gat_gtag_UA_123487620_1=1'
cookie_obj = httputils.get_cookie_from_str(cookie_obj)


post_data = {
'key': '上海楚千信息技术有限公',
'_': '1538218956336'
}

headers = {
    'Host': 'www.tianyancha.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host':'www.tianyancha.com'
}
#{"data":[{"id":27063827,"name":"<em>北京盛诺基医药科技有限</em>公司","type":1,"matchType":"公司名称匹配"},{"id":2343082190,"name":"青岛珅奥<em>基</em>生物工程<em>有限</em>公司","type":1,"matchType":"股东信息匹配"},{"id":27063722,"name":"<em>北京</em>恒<em>诺基医药科技有限</em>公司","type":1,"matchType":"股东信息匹配"},{"id":2310780535,"name":"武汉友芝友生物制<em>药有限</em>公司","type":1,"matchType":"股东信息匹配"},{"id":27854067,"name":"<em>北京</em>欣<em>诺基医药科技有限</em>公司","type":1,"matchType":"股东信息匹配"}],"state":"ok"}
reqs = httputils.get_req(req_url,data=post_data,cookies=cookie_obj,headers=headers)
print(reqs.content)











