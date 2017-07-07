```
     _           _                     _                 _ 
  __| |_ __   __| | _____      ___ __ | | ___   __ _  __| |
 / _` | '_ \ / _` |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |
| (_| | |_) | (_| | (_) \ V  V /| | | | | (_) | (_| | (_| |
 \__,_| .__/ \__,_|\___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|
      |_|                v-0.0.1                              让我们表现的...你被耍了
```

## 介绍

* 抓取免费代理，并保存到指定路径
* 配置代理文件，可选是否使用代理请求网址
  * 每次请求，轮询更换代理，防止代理被封
  * 代理不可用自动更换下一个
  
## 抓取免费代理

* 免费代理获取【西刺免费代理IP】: [http://www.xicidaili.com/nn/1](http://www.xicidaili.com/nn/1)
* 如果网站 HTML 有变化，会导致正则匹配出问题，届时会跟新版本

#### 代码示例

```python
# coding: utf-8

from dpdownload import download_proxy

# def download_proxy(testUrl, proxyFilePath, counts, startPage=1, timeout=5):
#    '''
#    :param testUrl: Check whether the agent can request the URL normally 
#    :param proxyFilePath: Finally save the path to the proxy file
#    :param counts: Page counts
#    :param startPage: The number of pages starting 
#    :param timeout: timeout
#    '''

download_proxy('http://www.tmtpost.com', '/root/proxy.txt', 2)

# testUrl 就是检查获取的代理是否在 timeout 内，可以正确请求该网址，通过则保留，否则遗弃

# 这里我们从【西刺免费代理IP】第1页，共抓取2页代理，
# 并检查获取的代理是否可以正确请求【钛媒体】首页，超时是5秒
# 将检查后的代理保存到 /root/proxy.txt
```

* --> [test_proxy.py](https://github.com/doupengs/dpdownload/blob/master/test/test_proxy.py)
* --> [proxy.txt](https://github.com/doupengs/dpdownload/blob/master/test/proxy.txt)

#### 信息展示

```
[DEBUG] 2017-07-07 17:16:23 threading.py __bootstrap_inner [line 774]: target [-] http://www.xicidaili.com/nn/1
[DEBUG] 2017-07-07 17:16:23 threading.py __bootstrap_inner [line 774]: target [-] http://www.xicidaili.com/nn/2
[INFO] 2017-07-07 17:16:23 test.py download_proxy [line 5]: raw proxy list - 200
[DEBUG] 2017-07-07 17:16:23 test.py download_proxy [line 5]: check url [-] http://www.tmtpost.com
[DEBUG] 2017-07-07 17:16:24 threading.py __bootstrap_inner [line 774]: checked [-] https://182.96.195.174:8118
[DEBUG] 2017-07-07 17:16:24 threading.py __bootstrap_inner [line 774]: checked [-] https://49.83.207.245:808
...
...
[DEBUG] 2017-07-07 17:16:44 threading.py __bootstrap_inner [line 774]: checked [-] https://115.220.150.198:808
[DEBUG] 2017-07-07 17:16:45 threading.py __bootstrap_inner [line 774]: checked [-] https://119.5.0.27:808
[INFO] 2017-07-07 17:16:46 test.py download_proxy [line 5]: checked proxy list - 130
[INFO] 2017-07-07 17:16:46 test.py download_proxy [line 5]: write to file succeed [-] /root/proxy.txt
```

## 请求网址（关闭代理）

#### 代码示例

```python
# coding: utf-8

from dpdownload import Download

url = 'http://www.tmtpost.com/'
dl = Download('/root/proxy.txt')
response = dl.download('GET', url)
print response

# def download(self, method, url, proxyEnable=False, **kwargs):
#     '''
#     :param method: 'GET','POST','PUT','DELETE','HEAD','OPTIONS'
#     :param url: url
#     :param proxyEnable: use proxy or not
#     :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`
#     :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`
#     :param json: (optional) json data to send in the body of the :class:`Request`
#     :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`
#     :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`
#     :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``)
#                   for multipart encoding upload.``file-tuple`` can be a 2-tuple ``('filename', fileobj)``,
#                   3-tuple ``('filename', fileobj, 'content_type')``or a 4-tuple ``('filename', fileobj,
#                   'content_type', custom_headers)``, where ``'content-type'`` is a string defining the
#                   content type of the given file and ``custom_headers`` a dict-like object containing
#                   additional headers to add for the file
#     :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth
#     :param timeout: (optional) How long to wait for the server to send data
#                     before giving up, as a float, or a :ref:`(connect timeout, read
#                     timeout) <timeouts>` tuple <float or tuple>
#     :param allow_redirects: (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed <class bool>
#     :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy
#     :param verify: (optional) whether the SSL cert will be verified. A CA_BUNDLE path can also be provided. Defaults to ``True``
#     :param stream: (optional) if ``False``, the response content will be immediately downloaded
#     :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair
#     :return: Response if failed Response=None
#     '''
```

* --> [test_download_without_proxy.py](https://github.com/doupengs/dpdownload/blob/master/test/test_download_without_proxy.py)

#### 结果展示

```
<Response [200]>
```

## 请求网址（使用代理）

#### 代码示例

```python
# coding: utf-8

from dpdownload import Download

url = 'http://www.tmtpost.com/'
dl = Download('/root/proxy.txt')
for i in xrange(5):
    response = dl.download('GET', url, True)
    print response
```

* --> [test_download_with_proxy.py](https://github.com/doupengs/dpdownload/blob/master/test/test_download_with_proxy.py)

#### 结果展示

```
[DEBUG] 2017-07-07 17:38:22 test.py download [line 8]: USE PROXY [-] https://182.96.195.174:8118
<Response [200]>
[DEBUG] 2017-07-07 17:38:23 test.py download [line 8]: USE PROXY [-] https://49.83.207.245:808
<Response [200]>
[DEBUG] 2017-07-07 17:38:23 test.py download [line 8]: USE PROXY [-] https://175.155.235.38:808
<Response [200]>
[DEBUG] 2017-07-07 17:38:23 test.py download [line 8]: USE PROXY [-] https://123.163.163.68:808
<Response [200]>
[DEBUG] 2017-07-07 17:38:23 test.py download [line 8]: USE PROXY [-] https://175.171.71.7:80
<Response [200]>
```

## 安装

#### 依赖的库

* requests
  * pip install requests
* dplog
  * [下载](https://github.com/doupengs/dplog/tree/master/dist)
  * pip install dplog-x.x.x.tar.gz
