from site_specific_parsing import returnJsonFromBulkSupplements
from site_specific_parsing import returnJsonFromJsonDumpFile
from site_specific_parsing import returnItemInfoBulkSupplementsJson
from site_specific_parsing import returnItemInfoFromHRNDJson
from site_specific_parsing import returnItemInfoFromMagentoSite
from site_specific_parsing import returnItemInfoNewStar
from site_specific_parsing import returnItemInfoPowderCity
import sys, os

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
    def __init__(self, _test): # check test
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

        self.skip_list = [] #'powdercity_urls','powdercitysingle_urls','peaknootropics','nootropicsdepot','nootropicscity','newstarnootropics','newmind','bulksupplements','hardrhino','liftmode'] # used to skip retailers
        self.txt_dir = os.getcwd()
        self.download_dir = os.getcwd() # retailer_name/downloaded_pages
        return

    def run(self):
        _test_err=[]
        # use self.split_dictionary 
        for retailer in self.split_dictionary.keys():
            # retailer in self.skip_list?
            if retailer in self.skip_list:
                continue
            dp = os.path.join(self.download_dir, retailer)
            for fn in os.listdir(dp):
                fp = os.path.join(dp, fn)
                
                leadsplit = self.split_dictionary[retailer][0]
                endsplit = self.split_dictionary[retailer][1]
                if _test:
                    size = os.stat(fp).st_size
                    r = "\nfn:",fn,"\nfp:",fp,"\nlead_split:",leadsplit,"\nend_split",endsplit, "\nf_size: ", size
                    if size is 0:
                        _test_err.append(r)
                    for t in r:
                        print("\nfn:",fn,"\nfp:",fp,"\nlead_split:",leadsplit,"\nend_split",endsplit, "\nf_size: ", size)
                else:
                    print(fn)
                    if retailer is 'hardrhino':
                        _json = returnJsonFromJsonDumpFile(fp)
                        returnItemInfoFromHRNDJson(_json) # change name duplicate
                    elif retailer is 'nootropicsdepot':
                        _json = returnJsonFromJsonDumpFile(fp)
                        returnItemInfoFromHRNDJson(_json) # change name duplicate
                    elif retailer is 'bulksupplements':
                        _json = returnJsonFromBulkSupplements(fp, leadsplit, endsplit)
                        returnItemInfoBulkSupplementsJson(_json)
                    elif retailer is 'liftmode':
                        returnItemInfoFromMagentoSite(fp)
                    elif retailer is 'newmind':
                        returnItemInfoFromMagentoSite(fp)
                    elif retailer is 'newstarnootropics':
                        returnItemInfoNewStar(fp)
                    elif retailer is 'nootropicscity':
                        returnItemInfoFromMagentoSite(fp)
                    elif retailer is 'peaknootropics':
                        returnItemInfoFromMagentoSite(fp)
                    elif retailer is 'powdercitysingle_urls':
                        returnItemInfoPowderCity(fp)
                    elif retailer is 'powdercity_urls':
                        returnItemInfoPowderCity(fp)
                    elif retailer is 'smartpowders':
                        returnItemInfoFromMagentoSite(fp)
        if _test:
            print(_test_err)
                    
if __name__=="__main__":
    Start(_test)
