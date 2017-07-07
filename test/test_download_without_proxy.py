# coding: utf-8

from dpdownload import Download

url = 'http://www.tmtpost.com/'
dl = Download('/root/proxy.txt')
response = dl.download('GET', url)
print response
