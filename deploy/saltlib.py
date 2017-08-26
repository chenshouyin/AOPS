#!/usr/bin/env python
#coding: utf-8

import urllib, urllib2
import json

class SaltAPI(object):
    def __init__(self, url, username, password):
        self.url = url
        self.user = username
        self.password = password

        self.token = self.get_token()
           
    def get_token(self):
        '''访问 https://127.0.0.1:8000/login，获取token——id
        '''
        param = {'eauth': 'pam', 'username': self.user, 'password': self.password}
        headers = urllib.urlencode(param)
        request = urllib2.Request(self.url+'/login', headers)
        response = urllib2.urlopen(request)
        content = json.loads(response.read())   #response.read() 返回字符串
        token = content['return'][0]['token']
        return token

    def request_entry(self, data):
        '''
        urllib2.Request(): __init__(self, url, data=None, headers={}, origin_req_host=None, unverifiable=False)
        '''

        headers = {'X-Auth-Token': self.token}

        request = urllib2.Request(self.url, data=data, headers = headers)
        response = urllib2.urlopen(request)
        result = response.read()
        return result


    def list_all_key(self):
        '''
            获取所有salt主机。包括认证、未认证的
        '''
        #-H "Accept: application/x-yaml" -H "X-Auth-Token: c8fed36186ef6f1ec3808816febf08f0f7e2acdf" -d client='wheel'  -d tgt='*' -d fun='key.list_all'
        param = {'client': 'wheel', 'fun': 'key.list_all'}
        data = urllib.urlencode(param)
        result = self.request_entry(data)
        return result

    def remote_execution(self, target_host, command):
        '''
        远程执行命令
        eg: saltapi.remote_execution(target="*", func="cmd.run", arg='ls')
        '''
        param = {'client': 'local', 'tgt': target_host, 'fun': 'cmd.run', 'arg': command}
        data = urllib.urlencode(param)
        result = json.loads(self.request_entry(data))
        return result['return'][0].values()

    def file_distribute(self, target_host, arg):
        '''
        功能：文件分发
        eg: saltapi.file_distribute(target="*", arg=["salt://backup/yantao", "/root/yantao"])
        该函数等同于：salt '*' cp.get_file salt://backup/yantao /root/yantao
        '''
        param = {'client': 'local', 'tgt': target_host, 'fun': 'cp.get_file'}
        data = urllib.urlencode(param)

        for i in arg:
            '''
            拼接URL参数.arg是多个参数时，需要拆分并加入到data中,
            eg: fun=cp.get_file&client=local&tgt=%2A&arg=salt%3A%2F%2Fbackup%2Fyantao&arg=%2Froot%2Fyantao
            '''
            temp = {'arg': i}
            data = "{}&{}".format(data, urllib.urlencode(temp))

        result = json.loads(self.request_entry(data))
        return result['return'][0].values()

    def salt_state(self, target, arg):
        '''
        执行sls 文件
        arg: sls文件名
        eg: saltapi.salt_state(target="*", arg="test")
        '''
        param = {'client': 'local', 'tgt': target, 'fun': 'state.sls', 'arg': arg}
        data = urllib.urlencode(param)
        print data
        result = self.request_entry(data)
        return result

    def check_alive(self):
        '''
        检测主机存活
        '''
        param = {'client': 'local', 'tgt': '*', 'fun': 'test.ping'}
        data = urllib.urlencode(param)
        result = self.request_entry(data)
        return result


if __name__ == "__main__":
    saltapi = SaltAPI('https://127.0.0.1:8000', username='saltapi', password='123456')
    #local_path = "salt://backup/yantao"
    #remote_path = "/root/yantao"
    #print saltapi.file_distribute(target="*", arg=[local_path, remote_path])
    print saltapi.remote_execution(target_host='*', command='ls')
