# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Description :
   Author :       xianyu123
   Creare_date：         2021/8/21 21:11
   Editor ：      Luz
   Change_date:          2021/8/28 12:11
-------------------------------------------------
   Change Activity:
                   2021/8/21 21:11
                   2021/8/28 12:11
-------------------------------------------------
"""
import requests
import re
import json
import datetime
import time
import urllib.request
url_login = "https://authserver.zjhu.edu.cn/cas/login?service=https%3A%2F%2Fmhall.zjhu.edu.cn%2Fwebroot%2Fdecision%2Fview%2Fform%3Fop%3Dh5%26viewlet%3Dxxkj%25252Fmobile%25252Fbpa%25252F%2525E5%252581%2525A5%2525E5%2525BA%2525B7%2525E6%252589%252593%2525E5%25258D%2525A1.frm1%252525A5%252525E5%252525BA%252525B7%252525E6%25252589%25252593%252525E5%2525258D%252525A1.frm"
url_submit = "https://mhall.zjhu.edu.cn/webroot/decision/view/form"
url_getSessionID = "https://mhall.zjhu.edu.cn/webroot/decision/view/form?op=h5&viewlet=xxkj%252Fmobile%252Fbpa%252F%25E5%2581%25A5%25E5%25BA%25B7%25E6%2589%2593%25E5%258D%25A1.frm#/form"
url_getConfID = "https://mhall.zjhu.edu.cn/webroot/decision/view/form?sessionID={sessionID}&op=fr_form&cmd=load_content&toVanCharts=true&fine_api_v_json=3&widgetVersion=1"
from Crypto.Cipher import AES
from Crypto import Random
import base64
def encode_passwd(passwd):
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16) 
    unpad = lambda s : s[0:-s[-1]]
    key = "key_value_123456".encode('utf-8')
    iv ="0987654321123456".encode('utf-8')
    passwd = pad(passwd)
    cipher = AES.new(key, AES.MODE_CBC, iv )
    cipherpasswd= cipher.encrypt(passwd.encode('utf-8'))
    cipherpasswd_base16=base64.b16encode(cipherpasswd)
    return cipherpasswd_base16.decode()
def dakaluz():
    username = "2018XXXXXX"
    password = encode_passwd("XXXXXX")#身份证后6位，不是统一平台密码

    headers_general = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.0; rv:72.0) Gecko/20100101 Firefox/72.0"
    }
    req = requests.Session()
    getRes = req.get(url = url_login,headers = headers_general)

    lt = re.search(r"<input type=\"hidden\" name=\"lt\" value=\"(.+)\".+",getRes.text).group(1)
    execution = re.search(r"<input type=\"hidden\" name=\"execution\" value=\"(.+)\".+",getRes.text).group(1)

    datas = {
        "password":password,
        "username":username,
        "lt":lt,
        "execution":execution,
        "_eventId":"submit"
    }

    postRes = req.post(url=url_login,data=datas,headers = headers_general)


    sessionGetRes = req.get(url = url_getSessionID, headers = headers_general)
    sessionID = re.search(r"get sessionID\(\) {return '(.+?)'},",sessionGetRes.text).group(1)

    headers_conf = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.0; rv:72.0) Gecko/20100101 Firefox/72.0",
        "responseType": "json"
    }
    confGetRes = req.get(url = url_getConfID.format(sessionID=sessionID),headers = headers_conf)
    #print(confGetRes.text)
    jsConfId = re.search(r"jsConfId:\"(.+?)\"",confGetRes.text).group(1)
    callbackConfId = re.search(r"callbackConfId:\"(.+?)\"",confGetRes.text).group(1)
    print(jsConfId)
    print(callbackConfId)
    today = str(datetime.date.today())
    # print(today)
    info=###
    #info自行抓包填充,包内容为提交信息，urldecode两次可以看到明文信息，这里使用只decode一次的中间明文，以上面格式替换中间变量
    datas = {
        "op":"dbcommit",
        "__parameters__":info
    }
    headers_submit = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.0; rv:72.0) Gecko/20100101 Firefox/72.0",
        "sessionID":sessionID,
        "__device__": "unknown"
    }

    submitRes = req.post(url=url_submit,headers = headers_submit,data=datas)
    #print(submitRes.text)
    if "提交成功" in submitRes.text:
        print("提交成功")

dakaluz()