# coding: utf-8

from dpdownload import Download

url = 'http://www.tmtpost.com/'
dl = Download('/root/proxy.txt')
for i in xrange(5):
    response = dl.download('GET', url, True)
    print response
