from site_specific_parsing import returnItemInfoFromSite
import sys, os, yaml

# loads as dictionary
# with open('product_urls','r') as f: data = y.safe_load(f)


try:
    _test = sys.argv[1]
    if _test:
        _test = True
        print('Testing ...')
except:
    _test = False
    print('Running...')


class Start(object):
    def __init__(self, _test, yaml_file, data): # check test
        self.yaml_file = self.returnYamlDict(yaml_file)
        self.data = data
        self._test = _test
        self.config()
        self.run()

    def config(self):
        '''
        '''
        # define this to skip parsing
        # used to skip retailers
        self.skip_list = ['powdercity','powdercitysingle', 'peaknootropics',
                          'nootropicsdepot','newstarnootropics','newmind',
                          'bulksupplements','hardrhino','liftmode', 'smartpowders'] # 'nootropicscity',
                    
        self.txt_dir = os.getcwd()
        self.download_dir = os.getcwd() # retailer_name/downloaded_pages
        return
        
    def returnYamlDict(self, yaml_file):
        try:
            with open(yaml_file,'r') as f:
                data = yaml.load(f)
            return data
        except Exception as e:
            import traceback;print(traceback.format_exc())
            exit()

    def run(self):
        _test_err=[]
        results = []
        _reval = {'peaknootropics':   {'units':'[x["value"] for x in soup.find_all("table",class_="variations")[0].find_all("option")]', #bs4 returnItemInfoFromMagentoSite
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
                  'liftmode':           {'units': [], #bs4 returnItemInfoFromMagentoSite
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
                  'newstarnootropics':{'units': '', #bs4
                                       'unit_of_measure': '',
                                       'prices': '',
                                       'product_name': '',
                                       'price': '',
                                       'products': '[product.text.split(" - ") for product in soup.find_all("option")]',
                                       '_type': 'bs4'
                                       },
                  'powdercity':        {'units': '', #bs4
                                       'unit_of_measure': '',
                                       'prices': '',
                                       'product_name': 'soup.find_all("h1", id="product-title")[0].next',
                                       'price': 'soup.find_all("span", itemprop="price")[0].next',
                                       '_type': 'bs4'
                                       },
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

        # use self.split_dictionary 
        for retailer in _reval.keys():
            name = None
            price = None
            items = None
            # retailer in self.skip_list?
            if retailer in self.skip_list:
                continue
            dp = os.path.join(self.download_dir, retailer)
            for fn in os.listdir(dp):
                fp = os.path.join(dp, fn)                
                # if _test print out relevant fp and dict info
                if _test:
                    size = os.stat(fp).st_size
                    r = "\nfn:",fn,"\nfp:",fp,"\nlead_split:",leadsplit,"\nend_split",endsplit, "\nf_size: ", size
                    if size is 0:
                        _test_err.append(r)
                    for t in r:
                        print("\nfn:",fn,"\nfp:",fp,"\nlead_split:",leadsplit,"\nend_split",endsplit, "\nf_size: ", size)
                else:
                    product_name = fn.replace('_',' ')
                    _multi = self.data[retailer][product_name]['multi_size']
                    _dict = self.data[retailer][product_name]
                    items = returnItemInfoFromSite(fp,retailer=retailer, _reval=_reval,_multi=_multi, _dict=_dict)
                    results.append([retailer, product_name, name, price, items, self.data[retailer][product_name]])
        import pdb;pdb.set_trace()
        if _test:
            print(_test_err)
                    
if __name__=="__main__":
    Start(_test)
