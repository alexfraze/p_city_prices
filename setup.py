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
      ],
      dependency_links = ['https://github.com/Shopify/shopify_python_api/tarball/master#egg=shopify'],
     )

