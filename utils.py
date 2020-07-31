import requests
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, Timeout
import json

class HTTPRequest:
    def __init__(self, url):
        self.url = url
        self.session = Session()
        self.exc_fname = ''
        self.__max_retries = 3
        self.session.mount(self.url, HTTPAdapter(max_retries=self.__max_retries))

    def get(self, url, params, headers={}, exc_fname='', timeout=20, raw=False):
        self.exc_fname = exc_fname
        try:
            r = self.session.get(url=url, params=params, timeout=timeout, headers=headers)
            r.raise_for_status()
            if not raw:
                return_value = r.json()
            else:
                return_value = r
        except Exception as e:
            log(e, r, self.exc_fname)
            if not raw:
                return_value = {}
        return return_value

def log(e, log_str, log_f, mode='a'):
    with open(log_f, mode) as f:
        f.write('{0}\n{1}\n\n'.format(e, log_str))
    return