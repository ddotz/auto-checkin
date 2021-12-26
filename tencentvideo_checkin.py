# -*- coding: utf8 -*-
import requests
import requests.utils
import time
import json
import os


def tencent_video_sign_in():
    """
    腾讯视频签到函数
    """
    millisecond_time = round(time.time() * 1000)
    vappid = os.environ.get('vappid')
    vsecret = os.environ.get('vsecret')
    g_vstk = os.environ.get('g_vstk')
    g_actk = os.environ.get('g_actk')
    vqq_vuserid = os.environ.get('vqq_vuserid')
    vqq_openid = os.environ.get('vqq_openid')
    vqq_access_token = os.environ.get('vqq_access_token')
    vqq_vusession = os.environ.get('vqq_vusession')
    test_hello = os.environ.get('test')
    print(test_hello)
    print(vappid,'\n', vsecret,'\n', g_vstk,'\n', g_actk,'\n', vqq_vuserid,'\n', vqq_access_token,'\n', vqq_vusession)
    login_url = "https://access.video.qq.com/user/auth_refresh" \
                f"?vappid={vappid}" \
                f"&vsecret={vsecret}" \
                "&type=qq" \
                f"&g_vstk={g_vstk}" \
                f"&g_actk={g_actk}" \
                f"&_={millisecond_time}"

    login_cookie = f"vqq_vuserid={vqq_vuserid}; " \
                   f"vqq_openid={vqq_openid}; " \
                   f"vqq_access_token={vqq_access_token}; " \
                   f"vqq_vusession={vqq_vusession}; "

    login_headers = {
        'Referer': 'https://v.qq.com',
        'Cookie': login_cookie
    }

    login_rsp = requests.get(url=login_url, headers=login_headers)
    login_rsp_cookie = requests.utils.dict_from_cookiejar(login_rsp.cookies)
    print(login_rsp_cookie)
    if login_rsp.status_code == 200 and login_rsp_cookie:
        auth_cookie = "main_login=qq; " \
                      f"vqq_vusession={login_rsp_cookie['vqq_vusession']}; "

        print(auth_cookie)
        sign_in_url = "https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2" \
                      f"&_={str(millisecond_time)}"

        sign_headers = {
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; Mi Note 3 Build/OPM1.171019.019) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 "
                          "Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.0.2",
            "Cookie": auth_cookie
        }
        sign_rsp = requests.get(url=sign_in_url, headers=sign_headers)
        sign_rsp_str = sign_rsp.text
        # QZOutputJson=({ "ret": 0,"checkin_score": 0,"msg":"OK"});
        # QZOutputJson=({"msg":"Account Verify Error","ret":-10006});
        start_index = sign_rsp_str.index("(")
        end_index = sign_rsp_str.index(")")
        rsp_dict = json.loads(sign_rsp_str[start_index + 1:end_index])

        if rsp_dict.get("ret") == -10006:
            result_msg = "腾讯视频-签到结果:{}".format("Cookie无效！")
        elif rsp_dict.get("ret") == 0:
            result_msg = "腾讯视频-签到结果:{}({})".format("签到成功！", rsp_dict.get("checkin_score"))
        else:
            result_msg = "腾讯视频-签到结果:{}".format("未知错误！！！")
    else:
        result_msg = "腾讯视频-签到结果:{}".format("未获取到Cookie信息！")
    print(result_msg)
    return result_msg


def weixin_notification(msg):
    token = os.environ.get('wx_token')
    uid = os.environ.get('wx_uid')
    url = "http://wxpusher.zjiecode.com/api/send/message"
    body = {
        "appToken": token,
        "content": msg,
        "contentType": 1,
        "uids": [
            f"{uid}"
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url=url, headers=headers, json=body)
    print(response.text)


def main_handler(event, context):
    result = tencent_video_sign_in()
    weixin_notification(result)
    return result


if __name__ == '__main__':
    print(os.environ.keys())
    weixin_notification(tencent_video_sign_in())

