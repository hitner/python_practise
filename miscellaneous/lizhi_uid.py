import urllib.request

fm = 70017363
"""
if len(sys.argv) < 2:
    print('please input the phone')
    exit()
else:
    fm = sys.argv[1]
"""
response = urllib.request.urlopen(f'http://www.lizhi.fm/{fm}/')

raw_body_:bytes = response.read()
raw_body = raw_body_.decode('utf-8')

result_list = re.compile(r"验证码\-\-\-[0-9]+").findall(raw_body)
if len(result_list):
    print(f'phone:{phone}, sms code:{result_list[0][-6:]}')
else:
    print(f'not find sms code for phone:{phone}')