import urllib3
import threading
from queue import Queue
import yaml
import os
import time
import sys
import argparse

def csvtoyaml(in_f, out_f):
    '''
    this converts a csv to yaml
    '''
    #retailer    url    product    unit_size    total_units    single_size    multi_size#

    with open(in_f ,'r') as f:
        lines = f.read().split('\n')
        lines = [line.split("\t") for line in lines]
    header = lines[0]
    retailer = header.index('retailer')
    url = header.index('url')
    product = header.index('product')
    unit_size = header.index('unit_size')
    total_units = header.index('total_units')
    single_size = header.index('single_size')
    multi_size = header.index('multi_size')
    prev_retailer = None
    _dict = {}
    for line in lines[1:]:
        if len(line) is not len(header): # zero length line
            continue
        test = _dict.get(line[retailer])
        if test is None:
            _dict.update({line[retailer]: {}})
        try:
            _dict[line[retailer]].update({line[product]: {'comp_name': 'COMPNAME',
                                                        'url': line[url], 
                                                        'product': 
                                                        line[product], 
                                                        'unit_size':
                                                        line[unit_size], 
                                                        'total_units'
                                                        : line[total_units], 
                                                        'single_size'
                                                        : line[single_size], 
                                                        'multi_size'
                                                        : line[multi_size],
                                                        }
                                        }
                                    )
        except Exception as e:
                
            import traceback;print(traceback.format_exc())
            print(e)
            exit()
        prev_retailer = retailer

    with open(out_f,'w+') as f:
        try:
            f.write( yaml.dump(_dict, default_flow_style=False))
        except Exception as e:
            import traceback;print(traceback.format_exc())
            print(e)
            exit()
    print("Done converting: %s to %s" % (in_f, out_f))

def downloadurls(data):
    '''
    Requires a dictionary
    {retailer: {product:{info...}}}
    runs a threaded downloaded with a harcoded limit of 500 connections
    '''
    # utility - spawn a thread to execute target for each args
    def run_parallel_in_threads(target, args_list):
        result = Queue()
        # wrapper to collect return value in a Queue
        def task_wrapper(*args):
            print(*args)
            result.put(target(*args))
        threads = [threading.Thread(target=task_wrapper, args=[args]) for args in args_list]
        for t in threads:
            time.sleep(.6)
            t.start()
        for t in threads:
            t.join()
        return result
    def fetch(retailer_dict):
        '''
        this is threaded and requires a dictionary
        '''
        retailer = retailer_dict['retailer']
        url = retailer_dict['url']
        product = retailer_dict['product']
        r = retailer, product, http.urlopen('GET',url), url
        return r

    def grabproducts(data, retailer, products):
        thread_list = []
        for product in products.keys():
            url = data[retailer][product]['url']
            retailer_dict = {'retailer':retailer,'product':product,'url':url}
            print(retailer_dict)
            thread_list.append(retailer_dict)
        results = run_parallel_in_threads(fetch, thread_list)
        return results
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
    http = urllib3.PoolManager(500, headers=user_agent) # 500 connections might be too little if more products are scraped
    # put the queues in results
    results = []
    for retailer in data.keys():
        products = data[retailer]
        downloaded = grabproducts(data, retailer, products)
        results.append(downloaded)
    page_status_errors = []
    for rq_i, retailer_q in enumerate(results):
        for product_q in results[rq_i].queue:
            retailer_name = product_q[0]
            product_name = product_q[1]
            status = product_q[2].status
            data = product_q[2].data
            _url = product_q[3]
            directory = retailer_name.replace(' ','_')
            fn = product_name.replace(' ','_')
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(os.path.join(directory, fn),'wb') as f:
                f.write(data)
            print("Fetched: %s from %s Status: %s" % (product_name, retailer, status))
            if status is not 200: # aka 404 or 50X
                page_status_errors.append([{'status':status,'_url':_url,'retailer_name':retailer_name,'product_name':product_name}])
    if len(page_status_errors) > 0:
        print("\n#########\n")
        print("The following pages were not downloaded (aka 404 not found, 503 service timed out or was denied):\n")
        for item in page_status_errors:
            print(item)
        while True:
            result = input("Would you like to continue? [y or n] and enter: ")
            if result is 'y':
                with open('./page_status_errors','w+') as f:
                    f.write(yaml.dump(page_status_errors))
                break
            elif result is 'n':
                exit()
            else:
                print("I don't understand.")

def readyml(in_f):
    try:
        with open(in_f,'r') as f:
            data = yaml.load(f)
        return data
    except Exception as e:
        if 'page_status' in in_f:
            return
        import traceback
        print(traceback.format_exc())


def run():
    parser = argparse.ArgumentParser(description="This program scrapes the specified websites contained with the prodcut_map.csv file.")
    parser.add_argument('-f','--force_download', help="Force the download", action="store_true")
    parser.add_argument('-D','--Debug', help="Debug", action="store_true")
    args = parser.parse_args()

    p_map = 'product_map.csv'
    yml_file = 'result.yml'
    page_status_errors = 'page_status_errors'
    csvtoyaml(p_map, yml_file)
    data = readyml(yml_file)
    if args.force_download:
        print("Beginning Download Process...")
        downloadurls(data) #TODO: add getmtime check for files and skip if less than, or add flag to force
    from parseSites import Start
    Debug = args.Debug
    print("Starting Site Parsing...")
    try:
        status_errors = readyml(page_status_errors)
    except:
        status_errors = None
        pass
    Start(Debug, yml_file, data, status_errors)

if __name__=="__main__":
    run()













