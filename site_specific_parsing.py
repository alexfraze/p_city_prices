import os, json
from bs4 import BeautifulSoup as BS

log = open('log','a+')

def readFile(fp):
    # if the file is zero length the url fetcher failed
    if os.stat(fp).st_size is 0:
        raise Exception("[ERROR] File zero length: Does the url still exist?" +
                        " Consider checking the following file.",fp)
    with open(fp,'r+',encoding='utf-8') as f:
        lines = f.read()
    return lines

def handleException(*args, **kwargs):
    #print(e, args, kwargs)
    if not os.path.exists('./DEBUG'):
        os.makedirs('./DEBUG')
    lines = kwargs['lines']
    soup = kwargs['soup']
    try:
        with open('./DEBUG/html','w+') as f:
            f.write(soup.prettify())
        print(kwargs['e'])
    except:
        pass
    #print(kwargs['d']['_reval'])
    for key in kwargs['d']:
        if key is '_reval':
            for _rkey in kwargs['d']['_reval']:
                print('{0}: {1}'.format(_rkey,kwargs['d']['_reval'][_rkey]))
            continue
        print('{0}: {1}'.format(key,kwargs['d'][key]))
    print(kwargs['e'])
    print(kwargs['t'])
    print('''
#
#
#
#
#############
The html file has been written out to './DEBUG/html'

By scrolling up if the _type is 'json' then 'soup' and 'lines'
will may not exist. Otherwise what this means is that the
scraper was unable to find the name or price. 

Pdb is a way to do inline debugging so all python one liners apply.
    (Pdb) kwargs.keys()
    dict_keys(['t', 'd', 'soup', 'e', 'lines'])
    t = traceback. By following the line numbers in the traceback
        we can figure out where it failed.
    d = a dictionary filled with product info
    e = the error
    lines = what was being parsed at the time of error

type: 'soup' and/or 'lines' to view the html
type: 'dir() to see what to work with
type: 'continue' to ignore the error
type: 'l' to see where we are in the code
type: 'h' to see pdb commands
type: 'args' or 'kwargs to see what info is available related to the item in question

If 'soup' and/or 'lines' is empty that means the page 
doesn't exist or failed to download

################
''')
    import pdb;pdb.set_trace()
    return

def returnJsonFromBulkSupplements(fp, leadsplit, endsplit):
    try:
        lines = readFile(fp)
    except Exception as e:
        _s = '\n'.join([e.args[0],e.args[1],''])
        log.write(_s)
        return None
    _json = lines.split(leadsplit)[1].split(endsplit)[0]
    _json = json.loads(_json)
    return _json
    
def returnJsonFromJsonDumpFile(fp):
    try:
        _json= readFile(fp)
    except Exception as e:
        raise Exception(e)
    _json = json.loads(_json)
    return _json

def returnItemInfoFromJson(_json, *args, **kwargs):
    '''
    print(_json.keys())
    print(_json['details'].keys())
    dict_keys(['details', 'success'])
    dict_keys(['sku', 'thumb', 'purchasable', 'baseThumb', 'unformattedPrice', 'unformattedRrp', 'upc', 'priceLabel', 'price', 'base', 'instock', 'baseImage', 'image', 'rrp'])
    '''
    fp = kwargs['fp']
    name = None
    price = None    
    # name(based on picture name in thumb image), price
    if _json is None:
        return
    name = _json['details']['thumb'].split('/')[-1].split('.')[0].split('__')[0]
    price = _json['details']['price']
    check_name_price(fp,name,price)
    return name,price

def check_error( e, fp, *args, **kwargs):
    # import pdb;pdb.set_trace()

    return

def check_name_price(fp, name, price):
    # check
    try:
        if (name is None) and (price is None):
            error = '[ERROR] Unable to find name and price: {0}'.format(fp)
            return False, error
        elif (name is None):
            error = '[ERROR] NAME MISSING: {0}'.format(fp)
            return False, error         
        elif (price is None):
            error = '[ERROR] Price MISSING: {0}'.format(fp)
            return False, error   
        else:
            #print('Parsed',fp,'\n',name, price)
            return True, None
    except Exception as e:
        # import pdb;pdb.set_trace()
        return False, e
        pass
    return

def returnItemInfoFromSite(fp, *args, **kwargs):
    '''
    '''
    retailer = kwargs['retailer']
    _reval = kwargs['_reval']
    _multi = kwargs['_dict']['multi_size']
    _type = _reval[retailer]['_type']
    handle_exceptions = kwargs['handle_exceptions']
    total_units_list = kwargs['_dict']['total_units'].split(',')
    name = None
    price = None
    units = None
    s_unit_of_measure = None
    prices = None
    s_product_name = None
    price = None
    soup = None
    lines = None
    return_dict = {'scraped_units': '', #str split
                  's_unit_of_measure': '',
                  'smulti_prices': '',
                  's_product_name': '',
                  'price': '',
                  'leadsplit': '',
                  'endsplit': '',
                  '_type': '',
                  'scraped_name':'',
                  'scraped_price':'',
                  }
    try:
        if retailer is 'bulksupplements':
            # import pdb;pdb.set_trace()
            items = []
            leadsplit = _reval[retailer]['leadsplit']
            endsplit = _reval[retailer]['endsplit']
            _json = returnJsonFromBulkSupplements(fp, leadsplit, endsplit)
            for item in _json['attributes']['134']['options']:
                for _id in _json['childProducts'].keys():
                        if _id in item['products'][0]:
                            name = item['label']
                            price = _json['childProducts'][_id]
                            product_id = _id # not used
                            check_name_price(fp,name,price)
                            items.append({"scraped_name": name,
                                          "scraped_price":price})
            return items
        if (retailer is 'hardrhino') or (retailer is 'nootropicsdepot'):
            _json = returnJsonFromJsonDumpFile(fp)
            s_product_name, price = returnItemInfoFromJson(_json, fp=fp)
            _r, _e = check_name_price(fp,s_product_name,price)
            if not _r:
                raise Exception(_e)
            return_dict.update({"scraped_name": s_product_name, "scraped_price":price})
            return return_dict
        if _type is 'bs4':
            # import pdb;pdb.set_trace()
            lines = readFile(fp)
            soup = BS(lines, 'html5lib')
            if 'True' in _multi:
                try:
                    units = eval(_reval[retailer]['units']) # Units
                    s_unit_of_measure = eval(_reval[retailer]['unit_of_measure']) # Unit of Measure
                    prices = eval(_reval[retailer]['prices']) #prices
                    if len(prices) is not len(total_units_list):
                        if len(units) is not len(prices):
                            raise Exception("[ERROR] Total units listed are not equal to the prices scraped")
                    s_product_name = eval(_reval[retailer]['product_name'])
                    return_dict.update({"scraped_units": units,
                                   "s_unit_of_measure":s_unit_of_measure,
                                   "smulti_prices": prices})
                    return return_dict
                except Exception as e:
                    raise e
            else:
                try:
                    s_product_name = eval(_reval[retailer]['product_name'])
                    price = eval(_reval[retailer]['price'])
                except Exception as e:
                    raise e
                _r, _e = check_name_price(fp,s_product_name,price)
                if not _r:
                    raise Exception(_e)
                return_dict.update({"scraped_name": s_product_name, "scraped_price":price})
                return return_dict
        check_name_price(fp,s_product_name,price)
    except Exception as e:
        import traceback
        t = traceback.format_exc()
        d = {'fp': fp,
             'retailer': retailer,
             '_multi': _multi,
             '_type': _type,
             'name': name,
             'price': price,
             'units': units,
             's_unit_of_measure': s_unit_of_measure,
             'prices': prices,
             's_product_name': s_product_name,
             '_reval': _reval[retailer],
            }
        if handle_exceptions:
            handleException(None,e=e, t=t, d=d, soup=soup, lines=lines)
        return_dict.update({"scraped_name": s_product_name, "scraped_price":price})
        return return_dict
    return_dict.update({"scraped_name": s_product_name, "scraped_price":price})
    return return_dict