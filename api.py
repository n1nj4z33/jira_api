# -*- coding: utf-8 -*-
'''
A python wrapper for the Jira 6.x REST API
For more information see https://www.atlassian.com/software/jira
'''
import requests
from requests.utils import urlparse
import logging

def prepare_logger():
    '''Prepare module logger'''
    inner_logger = logging.getLogger(__name__)
    inner_logger.setLevel(logging.DEBUG)
    chanel = logging.StreamHandler()
    chanel.setLevel(logging.DEBUG)
    inner_logger.addHandler(chanel)
    return inner_logger

LOGGER = prepare_logger()

class JiraAPI(object):
    '''Class for communication with jira'''
    def __init__(self, url):
        self.base_url = urlparse(url).netloc
        self.url = 'http://%s' % self.base_url
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})

    def prepare_url(self, url):
        '''Prepare url from methods url'''
        return '/'.join((self.url, url))

    def send_request(self, url=None, method=None, headers=None, data=None, auth=None):
        '''Send request and logging the response. Returns Response Object'''
        url = self.prepare_url(url)
        LOGGER.info('Request url: %s', url)
        LOGGER.info('Request data: %s', data)
        response = self.session.request(method=method,
                                        url=url,
                                        headers=headers,
                                        data=data,
                                        auth=auth,
                                        verify=False)
        LOGGER.info('Response code: %s', response.status_code)
        LOGGER.info('Response text: %s', response.text)
        return response

    def httpauth(self, username, password):
        '''HTTP authorization'''
        auth = requests.auth.HTTPBasicAuth(username,
                                           password)
        url = self.prepare_url('httpAuth/')
        return self.session.post(url=url,
                                 auth=auth)
  
