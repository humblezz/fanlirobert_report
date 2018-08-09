import datetime
import getopt
import json
import sys
import time

import requests

import os
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import threading
from urllib import parse

host = 'http://117.41.182.18:8888/'
download_folder = 'E:\短信发送\download'


class Spider(object):
    def __init__(self):

        self.web = webdriver.Chrome()
        self.headers = {
            'accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'accept-encoding':
            'gzip, deflate',
            'accept-language':
            'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'cache-control':
            'max-age=0',
            'upgrade-insecure-requests':
            '1',
            'Referer':
            'http://117.41.182.18:8888/outbox.asp',
            'user-agent':
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        }
        self.req = requests.Session()
        self.cookies = {}

    def qs(self, url):
        query = parse.urlparse(url).query
        return dict([(k, v[0]) for k, v in parse.parse_qs(query).items()])

    def login(self):
        print('begin login')
        self.web.get('http://117.41.182.18:8888/index.asp')
        while True:
            print('sleep 20 seconds')
            time.sleep(20)
            print('wait for user login user')
            if self.web.current_url == 'http://117.41.182.18:8888/main.asp':
                print(self.web.current_url)
                break

        self.web.get('http://117.41.182.18:8888/outbox.asp')
        time.sleep(10)
        cookie = ''
        for elem in self.web.get_cookies():
            cookie += elem["name"] + "=" + elem["value"] + ";"
            if elem["name"] == '_tb_token_':
                self.token = elem["value"]
        self.cookies = cookie
        self.headers['Cookie'] = self.cookies
        self.web.quit()

    def get_send_list(self):
        links = []
        # sSend_Content=&sFrom=2017-07-06&sTo=2018-07-06&sChannel_ID=
        page_param = {
            'sSend_Content': '',
            'sFrom': '2017-07-06',
            'sTo': '2018-07-06',
            'sChannel_ID': ''
        }
        first_load = self.req.post(
            'http://117.41.182.18:8888/outbox.asp',
            data=page_param,
            headers=self.headers)
        html = BeautifulSoup(first_load.content, 'html.parser')
        last_page_link = html.select('td[class="listtail"] > a')[1]
        link = BeautifulSoup(str(last_page_link), 'html.parser')
        link_href = link.a.attrs['href']
        print(link_href)

        params_dic = self.qs(link_href)
        max_page_number = int(params_dic['pageid'])
        for i in range(1, max_page_number + 1):
            page_url = host + 'outbox.asp?pageid=' + str(
                i) + '&sChannel_ID=' + str(
                    params_dic['sChannel_ID']
                ) + '&sFrom=2017-07-06&sTo=2018-07-30&sSend_Content='
            links.append(page_url)
        return links
        # http://117.41.182.18:8888/outbox.asp?pageid=10&sChannel_ID=1&sFrom=2017-07-25&sTo=2018-07-08&sSend_Content=
        # ?pageid=12&sChannel_ID=1&sFrom=2017-12-01&sTo=2018-07-06&sSend_Content=

    def get_phone_detail_links(self, links):
        file_links = []
        for pagelink in links:
            page_res = self.req.get(pagelink, headers=self.headers)
            html = BeautifulSoup(page_res.content, 'html.parser')
            detail_links = html.find_all(href=re.compile(r'getsendfile.asp\?'))
            file_links.extend(detail_links)

        return file_links

    def download_phone_txt(self, file_links):
        for file_link in file_links:
            file_a_tag = BeautifulSoup(str(file_link), 'html.parser')
            file_href = file_a_tag.a.attrs['href']
            params_dic = self.qs(file_href)
            phone_num_res = self.req.get(
                host + file_href, headers=self.headers)
            filename = os.path.join(download_folder,
                                    str(params_dic['File_ID']) + '.txt')
            print(filename)
            with open(filename, 'wb+') as phone_txt:
                phone_txt.write(phone_num_res.content)


if __name__ == '__main__':
    sp = Spider()
    sp.login()
    page_links = sp.get_send_list()
    file_links = sp.get_phone_detail_links(page_links)
    sp.download_phone_txt(file_links)