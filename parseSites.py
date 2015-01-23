from site_specific_parsing import returnJsonFromBulkSupplements
from site_specific_parsing import returnJsonFromJsonDumpFile
from site_specific_parsing import returnItemInfoBulkSupplementsJson
from site_specific_parsing import returnItemInfoFromHRNDJson
from site_specific_parsing import returnItemInfoFromMagentoSite
from site_specific_parsing import returnItemInfoNewStar
from site_specific_parsing import returnItemInfoPowderCity
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
        ---------------------------------------------------
        # self.split_dictionary = { 'dirname_sitename',[leadsplit, endsplit]}
        # originally implemented for string based parsing
        # the only supplier that actually uses it is bulk supplements
        # #TODO: consider renaming 
        # but now includes, json, and BS4 parsing as well
        ---------------------------------------------------
        '''
        self.split_dictionary = {
                    'bulksupplements':['Product.Config(',");"],
                    'hardrhino':['already_json',None],
                    'nootropicsdepot':['already_json',None], # similar to hardrhino ... almost exactly the same
                    'liftmode':['magento_based_site',None],
                    'newmind':['magento_based_site',None],
                    'newstarnootropics':['custom_site',None],
                    'nootropicscity':['magento_based_site',None],
                    'peaknootropics':['magento_based_site',None],
                    'powdercity':['shopify_based_site',None],
                    'smartpowders':['magento_based_site',None]
                    }
        # define this to skip parsing
        # used to skip retailers
        self.skip_list = []#'powdercity_urls','powdercitysingle_urls','peaknootropics',
                          #'nootropicsdepot','nootropicscity','newstarnootropics','newmind',
                          #'bulksupplements','hardrhino','liftmode'] #,'liftmode'
                    
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
        # use self.split_dictionary 
        for retailer in self.split_dictionary.keys():
            name = None
            price = None
            items = None
            # retailer in self.skip_list?
            if retailer in self.skip_list:
                continue
            dp = os.path.join(self.download_dir, retailer)
            for fn in os.listdir(dp):
                fp = os.path.join(dp, fn)                
                leadsplit = self.split_dictionary[retailer][0]
                endsplit = self.split_dictionary[retailer][1]
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
                    if retailer is 'hardrhino':
                        _json = returnJsonFromJsonDumpFile(fp)
                        items = returnItemInfoFromHRNDJson(_json, fp=fp) # change name duplicate
                    elif retailer is 'nootropicsdepot':
                        _json = returnJsonFromJsonDumpFile(fp)
                        items = returnItemInfoFromHRNDJson(_json, fp=fp) # change name duplicate
                    elif retailer is 'bulksupplements':
                        _json = returnJsonFromBulkSupplements(fp, leadsplit, endsplit)
                        items = returnItemInfoBulkSupplementsJson(_json, fp=fp)
                    elif retailer is 'liftmode':
                        if _multi is True:
                            print("THIS SHOULD HAVE MULTIPLE SIZES1")
                        name, price = returnItemInfoFromMagentoSite(fp, retailer=retailer, _dict=self.data[retailer][product_name])
                    elif retailer is 'newmind':
                        if _multi is True:
                            print("THIS SHOULD HAVE MULTIPLE SIZES2")                        
                        name, price = returnItemInfoFromMagentoSite(fp, retailer=retailer, _dict=self.data[retailer][product_name])
                    elif retailer is 'newstarnootropics':
                        proportion_list = returnItemInfoNewStar(fp)
                        last_proportion_list = self.yaml_file[retailer][product_name]['total_units'].split(', ')
                        #if proportion_list is last_proportion_list:
                            #print(proportion_list, last_proportion_list)
                    elif retailer is 'nootropicscity':
                        if _multi is True:
                            print("THIS SHOULD HAVE MULTIPLE SIZES3")                        
                        name, price = returnItemInfoFromMagentoSite(fp, retailer=retailer, _dict=self.data[retailer][product_name])
                    elif retailer is 'peaknootropics':
                        if _multi is True:
                            print("THIS SHOULD HAVE MULTIPLE SIZES4")
                        name, price = returnItemInfoFromMagentoSite(fp, retailer=retailer, _dict=self.data[retailer][product_name])
                    elif retailer is 'powdercity':
                        if _multi is True:
                            print("THIS SHOULD HAVE MULTIPLE SIZES5")
                        name, price = returnItemInfoPowderCity(fp)
                    elif retailer is 'smartpowders':
                        if _multi is True:
                            print("THIS SHOULD HAVE MULTIPLE SIZES6")             
                        name, price = returnItemInfoFromMagentoSite(fp, retailer=retailer, _dict=self.data[retailer][product_name])
                    results.append([retailer, product_name, name, price, items, self.data[retailer][product_name]])
        import pdb;pdb.set_trace()
        if _test:
            print(_test_err)

                    
if __name__=="__main__":
    Start(_test)
