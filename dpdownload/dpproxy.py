# coding: utf-8

import re
import threading
import requests
from dplog import logger


_RAW_PROXY_LIST = []
_CHECKED_PROXY_LIST = []
_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}
_PATTERN = r'<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,4})</td>.+?<td>(.{4,5})</td>'


class ProxyGet(threading.Thread):
    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target

    def getProxy(self):
        logger.debug('target [-] %s' % self.target)
        session = requests.session()
        response = session.get(url=self.target, headers=_HEADERS)
        response.encoding = 'utf-8'
        result= re.findall(_PATTERN, response.text, re.DOTALL)
        for row in result:
            ip = row[0]
            port = row[1]
            agent = row[2].lower()
            proxy = (agent, ip, port)
            _RAW_PROXY_LIST.append(proxy)

    def run(self):
        self.getProxy()


class ProxyCheck(threading.Thread):
    def __init__(self, proxyList, testUrl, timeout=5):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = timeout
        self.testUrl = testUrl

    def checkProxy(self):
        session = requests.session()
        for proxy in self.proxyList:
            proxies = {proxy[0]: "%s://%s:%s" % (proxy[0], proxy[1], proxy[2])}
            try:
                res = session.get(url=self.testUrl, proxies=proxies, headers=_HEADERS, timeout=self.timeout)
                if res.status_code == 200:
                    logger.debug('checked [-] %s' % proxies[proxy[0]])
                    _CHECKED_PROXY_LIST.append("%s://%s:%s" % (proxy[0], proxy[1], proxy[2]))
                else:
                    continue
            except:
                continue

    def run(self):
        self.checkProxy()


def download_proxy(testUrl, proxyFilePath, counts, startPage=1, timeout=5):
    '''
    :param testUrl: Check whether the agent can request the URL normally 
    :param proxyFilePath: Finally save the path to the proxy file
    :param counts: Page counts
    :param startPage: The number of pages starting 
    :param timeout: timeout
    '''
    getLoop   = []
    checkLoop = []
    for page in xrange(startPage, startPage+counts):
        target = "http://www.xicidaili.com/nn/%d" % page
        t = ProxyGet(target)
        getLoop.append(t)
        t.start()
    for t in getLoop:
        t.join()
    logger.info("raw proxy list - %s" % len(_RAW_PROXY_LIST))
    logger.debug('check url [-] %s' % testUrl)
    i = 0
    while i < len(_RAW_PROXY_LIST):
        t = ProxyCheck(_RAW_PROXY_LIST[i:i+10], testUrl, timeout)
        i += 10
        checkLoop.append(t)
        t.start()
    for t in checkLoop:
        t.join()
    logger.info("checked proxy list - %s" % len(_CHECKED_PROXY_LIST))
    with open(proxyFilePath, 'w+') as f:
        for i in _CHECKED_PROXY_LIST:
            f.write(i + '\n')
    logger.info("write to file succeed [-] %s" % proxyFilePath)
