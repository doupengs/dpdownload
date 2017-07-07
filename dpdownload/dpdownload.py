#coding:utf-8

import requests
from requests.exceptions import ProxyError
from dplog import logger

# TODO: Optimize the algorithm for replacing the agent
#       Record the request time
#       discard when unavailable

class Download(object):
    """
    :class: use requests.request method, return response or None
    """
    def __init__(self, proxyFilePath=None):
        """
        :param proxyFilePath: proxy file path
        :The correct format in the proxy file is as follows:
            http[s]://ip:port
        """
        self.proxies = []
        try:
            if proxyFilePath is None:
                logger.warning('No initialization proxy file path')
            else:
                with open(proxyFilePath, "r") as f:
                    proxies =  f.readlines()
                self.proxies = [p.strip() for p in proxies if p.startswith('http:') or p.startswith('https:')]
        except Exception as e:
            logger.error(e)

    def download(self, method, url, proxyEnable=False, **kwargs):
        '''
        :param method: 'GET','POST','PUT','DELETE','HEAD','OPTIONS'
        :param url: url
        :param proxyEnable: use proxy or not
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`
        :param json: (optional) json data to send in the body of the :class:`Request`
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`
        :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`
        :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``)
                      for multipart encoding upload.``file-tuple`` can be a 2-tuple ``('filename', fileobj)``,
                      3-tuple ``('filename', fileobj, 'content_type')``or a 4-tuple ``('filename', fileobj,
                      'content_type', custom_headers)``, where ``'content-type'`` is a string defining the
                      content type of the given file and ``custom_headers`` a dict-like object containing
                      additional headers to add for the file
        :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth
        :param timeout: (optional) How long to wait for the server to send data
                        before giving up, as a float, or a :ref:`(connect timeout, read
                        timeout) <timeouts>` tuple <float or tuple>
        :param allow_redirects: (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed <class bool>
        :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy
        :param verify: (optional) whether the SSL cert will be verified. A CA_BUNDLE path can also be provided. Defaults to ``True``
        :param stream: (optional) if ``False``, the response content will be immediately downloaded
        :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair
        :return: Response if failed Response=None
        '''
        if (not proxyEnable) or (proxyEnable and not self.proxies):
            if proxyEnable and not self.proxies:
                logger.warning('No initialization proxy file or proxy file is not available')
            try:
                return requests.request(method, url, **kwargs)
            except Exception as e:
                logger.warning(e)
        else:
            try:
                oneProxy = self.proxies.pop(0)
                self.proxies.append(oneProxy)
                key = oneProxy.split(":")[0]
                oneProxy = {key: oneProxy}
                logger.debug('USE PROXY [-] %s' % oneProxy.values()[0])
                return requests.request(method, url, proxies=oneProxy, **kwargs)
            except ProxyError:
                return self.download(method, url, proxyEnable, **kwargs)
            except Exception as e:
                logger.warning(e)
