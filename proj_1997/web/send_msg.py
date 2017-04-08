# -*- utf8 -*-
import requests
from .database_lib import get_msg_settings

send_msg_error = {
    0: '成功',
    1: '含有敏感词汇',
    2: '余额不足',
    3: '没有号码',
    4: '包含sql语句',
    10: '账号不存在',
    11: '账号注销',
    12: '账号停用',
    13: 'IP鉴权失败',
    14: '格式错误',
    -1: '系统异常'
}

def send_msg(code, mobile):
    name, pwd = get_msg_settings()
    content = '您的验证码是%s，如非本人操作，请忽略此条信息。' % code
    sign, type_ = '【1997家教】', 'pt'
    url = 'http://web.1xinxi.cn/asmx/smsservice.aspx'
    data = {
        'name': name,
        'pwd': pwd,
        'content': content,
        'mobile': mobile,
        'sign': sign,
        'type': type_,
        'sign': sign,
    }
    r = requests.post(url, data=data)
    print(r.text)
    c = int(r.text.split(',')[0])
    return c, send_msg_error[c]


if __name__ == '__main__':
    send_msg(code, mobile)