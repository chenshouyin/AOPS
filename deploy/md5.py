#!/usr/bin/env python
#coding: utf-8

import hashlib
import os

def md5(filename):
    '''
    计算文件的 md5 值
    '''

    if os.path.isfile(filename):
        hash_md5 = hashlib.md5()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    else:
        return "{} is not exists.".format(filename)

if __name__ == "__main__":
    print md5("/opt/saltapi.p")
