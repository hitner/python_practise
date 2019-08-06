#!/usr/local/bin/python3 
import urllib.request
import urllib.parse
import re
import sys

phone = '180001000'
if len(sys.argv) < 2:
    print('please input the phone')
    exit()
else:
    if(len(sys.argv[1]) == 2):
        phone =  phone + sys.argv[1]
    else:
        phone = sys.argv[1]


parames = {'env':1, "keyword":phone}
options_str = urllib.parse.urlencode(parames)

response = urllib.request.urlopen('http://j.lizhi.fm:8999/getcode',bytes(options_str, 'utf-8'))

raw_body_:bytes = response.read()
raw_body = raw_body_.decode('utf-8')

result_list = re.compile(r"验证码\-\-\-[0-9]+").findall(raw_body)
if len(result_list):
    print(f'phone:{phone}, sms code:{result_list[0][-6:]}')
else:
    print(f'not find sms code for phone:{phone}')
