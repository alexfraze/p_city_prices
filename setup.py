#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='Product Scraper',
      version='1.0',
      description='Specific Product Scraper',
      author='James Munsch',
      author_email='james.a.munsch@gmail.com',
      url='http://jamesmunsch.com/',
      install_requires=[
			"PyYAML>=3.11",
			"beautifulsoup4>=4.3.2",
			"html5lib>=0.999",
			"six>=1.8.0",
			"urllib3>=1.9.1",
                        "ShopifyAPI>=2.1.0",
			"paramiko",
      ],
      dependency_links = ['https://github.com/Shopify/shopify_python_api/tarball/master#egg=shopify'],
     )


import paramiko
import traceback
from getpass import getpass
class SshGetKeys(object):
    def __init__(self):
        super(SshGetKeys, self).__init__()
        self.getKeys()
    def setup(self):
        '''Setup connection'''
        try:
            print("\n\n########\nPlease enter the dev server login info found in keepass to pull shopify api keys.\n")
            self.username = input("Username: ")
            password = getpass("Password: ")
            host = "192.168.0.2"
            port = 22
            self.transport = paramiko.Transport((host, port))
            self.transport.connect(username = self.username, password = password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            print(self.sftp.sock)
        except Exception as e:
            print(traceback.format_exc())
        return False

    def getKeys(self):
        '''
        '''
        self.setup()
        try:
            self.sftp.get("/home/"+self.username+"/Desktop/shopify_keys.json", "../shopify_keys.json")
        except Exception as e:
            print(traceback.format_exc())
        self.close()
        return True

    def close(self):
        ''' Close the connection '''
        self.sftp.close()
        self.transport.close()
        return


SshGetKeys()