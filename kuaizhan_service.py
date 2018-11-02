import bottle
import os
import sys
from selenium import webdriver
import requests
import datetime
import json
import time
import logging
import random
import string
from bottle import route, run, TEMPLATE_PATH, default_app, template, static_file, get, error,view
from datetime import datetime
from paste import httpserver

if __name__ == '__main__':

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_path = os.path.dirname(os.path.realpath(__file__)) + '\\Logs\\'
    if os.path.exists(log_path) == False:
        os.makedirs(log_path)
    log_name = log_path + rq + 'kuaizhan.log'
    # 终端Handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)
    fileHandler = logging.FileHandler(log_name, mode="w")
    fileHandler.setLevel(logging.INFO)
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    kuaizhan_login_url = "https://www.kuaizhan.com/v3/passport/login"
    kuaizhan_site_list_url = "https://www.kuaizhan.com/v3/site"
    kuaizhan_site_off_url = "https://www.kuaizhan.com/site/ajax-offline?site_id={0}"
    kuaizhan_check_url = "https://www.kuaizhan.com/site/ajax-check-domain?domain={0}&site_id={1}"

    kuaizhan_publish_url = "https://www.kuaizhan.com/site/ajax-site-publish"

    chrome = webdriver.Chrome()
    req = requests.Session()

    kuaizhan_username = "account"
    kuaizhan_password = "password"

    kuaizhan_headers = {
        "Host": "www.kuaizhan.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://www.kuaizhan.com/v3/passport/login",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }

    chrome.get(kuaizhan_login_url)
    # time.sleep(2)
    username = chrome.find_element_by_name(name="userName")
    passwd = chrome.find_element_by_name(name="passwd")
    username.send_keys(kuaizhan_username)
    passwd.send_keys(kuaizhan_password)

    while True:
        logger.info('sleep 5 seconds, waiting for user login user' )
        time.sleep(5)
        if chrome.current_url == kuaizhan_site_list_url:
            logger.info("chrome current url:"+chrome.current_url)
            break

    cookie_str = ''
    cheome_cookies = chrome.get_cookies()
    for cookie in cheome_cookies:
        cookie_str += cookie["name"] + "=" + cookie["value"]+";"

    kuaizhan_headers["Cookie"] = cookie_str
    chrome.quit()

    @bottle.post("/kz_change")
    def change_kuaizhan_domain():
        json_req = bottle.request.json
        site_id = json_req["site_id"]
        logger.info("开始下线网站")
        offline_site_res = req.request(method="get", url=kuaizhan_site_off_url.format(
            site_id), headers=kuaizhan_headers)
        offline_json = offline_site_res.json()
        base_res = {'code': 1,
                    'msg': "kuaizhan change Successfully", 'data': {}}
        if offline_json["ret"] > 0:
            logger.info("domain offline ret:{0},msg:{1}".format(
                offline_json["ret"], offline_json["msg"]))
            base_res['code'] = -1
            base_res['msg'] = '域名下线失败：msg-->{0}'.format(offline_json["msg"])
            return base_res

        domain_name = ''.join(random.sample(
            string.ascii_letters + string.digits, 8))
        full_domain_name = "https://{0}.kuaizhan.com".format(domain_name)
        logger.info("domain name:"+full_domain_name)
        check_domain_res = req.request(method="get", url=kuaizhan_check_url.format(
            domain_name, site_id), headers=kuaizhan_headers)
        checkdomain_json = check_domain_res.json()
        if checkdomain_json["ret"] > 0:
            logger.info("check domain  ret:{0},msg:{1}".format(
                checkdomain_json["ret"], checkdomain_json["msg"]))
            base_res['code'] = -2
            base_res['msg'] = '检查域名已存在：msg-->{0}'.format(
                checkdomain_json["msg"])
            base_res['data'] = {'domain': full_domain_name}
            return base_res

        kuaizhan_pub = {
            "domain": domain_name,
            "industry": random.randint(1, 13),
            "area": random.randint(1, 34),
            "contract_read": "true",
            "site_id": site_id
        }
        site_pub_res = req.request(
            method="post", url=kuaizhan_publish_url, data=kuaizhan_pub, headers=kuaizhan_headers)
        if site_pub_res.status_code != 200:
            base_res['code'] = -3
            base_res['msg'] = '域名修改上线失败'
            base_res['data'] = {'domain': full_domain_name}
            return base_res
        logger.info("新域名已经上线："+full_domain_name)
        base_res['data'] = {'domain': full_domain_name}
        return base_res 

    httpserver.serve(bottle.default_app(), host=HOST, port=PORT)
