def evalSettings():

  _reval =  {'peaknootropics':   {'units':'[x["value"] for x in soup.find_all("table",class_="variations")[0].find_all("option")]', #bs4 returnItemInfoFromMagentoSite
                                'unit_of_measure': 'soup.find_all("table",class_="variations")[0].find("label").next',
                                'prices': 'soup.find_all(attrs={"class": "entry-summary"})[0].find_all("span",class_="amount")',
                                'product_name': 'soup.find_all("h1",itemprop="name")[0].next',
                                'price': 'soup.find("meta",itemprop="price").attrs["content"]',
                                '_type': 'bs4'
                                },
            'nootropicscity':   {'units': '', #bs4 returnItemInfoFromMagentoSite h2
                                'unit_of_measure': '',
                                'prices': '',
                                'product_name': 'soup.find_all("h2",itemprop="name")[0].next',
                                'price': 'soup.find("meta",itemprop="price").attrs["content"]',
                                '_type': 'bs4'
                                },
            'liftmode':           {'units': '', #bs4 returnItemInfoFromMagentoSite
                                  'unit_of_measure': '',
                                  'prices': '',
                                  'product_name': 'soup.find_all("h1",itemprop="name")[0].next',
                                  'price': 'soup.find("meta",itemprop="price").attrs["content"]',
                                  '_type': 'bs4'
                                  },
            'smartpowders':       {'units': '', #bs4 returnItemInfoFromMagentoSite
                                  'unit_of_measure': '',
                                  'prices': '',
                                  'product_name': 'soup.find_all("h1",itemprop="name")[0].next',
                                  'price': 'soup.find("meta",itemprop="price").attrs["content"]',
                                  '_type': 'bs4'
                                  },
            'newmind':          {'units': '', #bs4 returnItemInfoFromMagentoSite
                                 'unit_of_measure': '',
                                 'prices': '',
                                 'product_name': 'soup.find_all("h1",itemprop="name")[0].next',
                                 'price': 'soup.find("meta",itemprop="price").attrs["content"]',
                                 '_type': 'bs4'
                                 },
            'newstarnootropics':{'units': '[p[0] for p in [product.text.split(" - ") for product in soup.find_all("option")]]', #bs4
                                 'unit_of_measure': '[product.text.split(" - ") for product in soup.find_all("option")][0][0].split(" ")[2]',
                                 'prices': '[p[1] for p in [product.text.split(" - ") for product in soup.find_all("option")]]',
                                 'product_name': '[product.text.split(" - ") for product in soup.find_all("option")][0][0].split(" ")[-1]',
                                 'price': '',
                                 'products': '[product.text.split(" - ") for product in soup.find_all("option")]',
                                 '_type': 'bs4'
                                 },
            # 'powdercity':        {'units': '[s.split(' ') for s in [p.next for p in soup.find_all("option")]]', #bs4
            #                      'unit_of_measure': '',
            #                      'prices': '[p.next for p in soup.find_all("span", itemprop="price")]',
            #                      'product_name': 'soup.find_all("h1", id="product-title")[0].next',
            #                      'price': 'soup.find_all("span", itemprop="price")[0].next',
            #                      '_type': 'bs4'
            #                      },
              #'bulksupplements':['Product.Config(',");"],
            'bulksupplements':   {'units': '', #str split
                                  'unit_of_measure': '',
                                  'prices': '',
                                  'product_name': '',
                                  'price': '',
                                  'leadsplit': 'Product.Config(',
                                  'endsplit': ');',
                                  '_type': 'strsplit'
                                  },
            'nootropicsdepot':  {'units': '', #json
                                'unit_of_measure': '',
                                'prices': '',
                                'product_name': '',
                                'price': '',
                                '_type': 'json'
                                },
            'hardrhino':          {'units': '', #json
                                  'unit_of_measure': '',
                                  'prices': '',
                                  'product_name': '',
                                  'price': '',
                                '_type': 'json'
                                  },

            }
  return _reval