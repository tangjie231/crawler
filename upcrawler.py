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

print(reqs.content)
print(reqs.text)
print(reqs.cookies)
for cookie in reqs.cookies.items():
    print(cookie[0])
    print(cookie[1])











