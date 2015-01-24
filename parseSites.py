from site_specific_parsing import returnItemInfoFromSite
import sys, os, yaml
from _reval import evalSettings

print('Running...')

class Start(object):
    def __init__(self, Debug, yaml_file, data, status_errors):
        self.yaml_file = self.returnYamlDict(yaml_file)
        self.status_errors = status_errors
        self.data = data
        self.Debug = Debug
        self.config()
        self.run()

    def config(self):
        '''
        '''
        # define this to skip parsing
        # used to skip retailers
        self.skip_list = ['hardrhino']#'peaknootropics','nootropicscity','liftmode', 'smartpowders',
                          #'newmind','newstarnootropics','powdercitysingle', 'powdercity',
                          #'bulksupplements','nootropicsdepot'] # ,'hardrhino'
                    
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

    def debugInfo(self,*args,**kwargs):
        for key in kwargs['debug_dict'].keys():
            print("{0}: {1}".format(key, kwargs['debug_dict'][key]))

    def run(self):
        Debug_err=[]
        results = []
        _reval = evalSettings()
        for retailer in _reval.keys():
            print("Parsing: {0}".format(retailer))
            name = None
            price = None
            items = None
            # retailer in self.skip_list?
            if retailer in self.skip_list:
                continue
            dp = os.path.join(self.download_dir, retailer)
            for fn in os.listdir(dp):
                fp = os.path.join(dp, fn)                
                # if Debug print out relevant fp and dict info
                product_name = fn.replace('_',' ')
                _status_error = False
                for status_error in self.status_errors:
                    if (self.status_errors[0][0]['product_name'] in product_name) and (self.status_errors[0][0]['retailer_name'] in retailer):
                        print('Skipping: {0} {1} due to page_status_error {2}'.format(retailer,product_name,str(status_error)))
                        _status_error = True
                if _status_error:
                    continue
                _multi = self.data[retailer][product_name]['multi_size']
                _dict = self.data[retailer][product_name]
                items = returnItemInfoFromSite(fp,retailer=retailer, _reval=_reval,_multi=_multi, _dict=_dict)
                results.append([retailer, product_name, name, price, items, self.data[retailer][product_name]])
                if self.Debug:
                    size = os.stat(fp).st_size
                    debug_dict = {
                        "fp": fp,
                        "fn": fn,
                        "dp": dp,
                        "retailer": retailer,
                        "fp_size": size,
                        "_multi": _multi,
                        "_dict": _dict,
                        "items": items,
                    }
                    self.debugInfo(debug_dict=debug_dict)
        import pdb;pdb.set_trace()

                    
if __name__=="__main__":
    Start(Debug)
