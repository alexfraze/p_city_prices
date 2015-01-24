import os, json
from bs4 import BeautifulSoup as BS

log = open('log','a+')

def readFile(fp):
    # if the file is zero length the url fetcher failed
    if os.stat(fp).st_size is 0:
        raise Exception("[ERROR] File zero length: Does the url still exist?" +
                        " Consider checking the csv file.",fp)
    with open(fp,'r') as f:
        lines = f.read()
    return lines

def handleException(*args, **kwargs):
    #print(e, args, kwargs)
    if not os.path.exists('./DEBUG'):
        os.makedirs('./DEBUG')
    lines = kwargs['lines']
    soup = kwargs['soup']
    with open('./DEBUG/html','w+') as f:
        f.write(soup.prettify())
    print(kwargs['e'])
    #print(kwargs['d']['_reval'])
    for key in kwargs['d']:
        if key is '_reval':
            for _rkey in kwargs['d']['_reval']:
                print('{0}: {1}'.format(_rkey,kwargs['d']['_reval'][_rkey]))
            continue
        print('{0}: {1}'.format(key,kwargs['d'][key]))
    print(kwargs['e'])
    print(kwargs['t'])
    print('The html file has been written out to ./DEBUG/html and can be accessed with via soup and lines')
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
        _s = '\n'.join([e.args[0],e.args[1],''])
        log.write(_s)
        return None
    _json = json.loads(_json)
    return _json

    
def returnItemInfoFromHRNDJson(_json, *args, **kwargs):
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
    except:
        # import pdb;pdb.set_trace()
        pass
    return




def returnItemInfoFromSite(fp, *args, **kwargs):
    '''
    '''
    retailer = kwargs['retailer']
    _reval = kwargs['_reval']
    _multi = kwargs['_dict']['multi_size']
    _type = _reval[retailer]['_type']
    name = None
    price = None
    units = None
    unit_of_measure = None
    prices = None
    product_name = None
    price = None
    #import pdb;pdb.set_trace()
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
                            items.append([name,price])
            return items
        if _type is 'bs4':
            # import pdb;pdb.set_trace()
            lines = readFile(fp)
            soup = BS(lines, 'html5lib')
            if 'True' in _multi:
                try:
                    units = eval(_reval[retailer]['units']) # Units
                    unit_of_measure = eval(_reval[retailer]['unit_of_measure']) # Unit of Measure
                    prices = eval(_reval[retailer]['prices']) #prices
                    product_name = eval(_reval[retailer]['product_name'])
                    return units, unit_of_measure, prices
                except Exception as e:
                    raise e
            else:
                try:
                    product_name = eval(_reval[retailer]['product_name'])
                    price = eval(_reval[retailer]['price'])
                except Exception as e:
                    raise e
                _r, _e = check_name_price(fp,product_name,price)
                if not _r:
                    raise Exception(_e)
                return product_name, price
        elif _type is 'strsplit':
            startsplit = _reval[retailer]['startsplit']
            endsplit =   _reval[retailer]['endsplit']
            # import pdb;pdb.set_trace()
        elif _type is 'json':
            # import pdb;pdb.set_trace()
            pass
        check_name_price(fp,product_name,price)
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
             'unit_of_measure': unit_of_measure,
             'prices': prices,
             'product_name': product_name,
             '_reval': _reval[retailer],
            }
        handleException(None,e=e, t=t, d=d, soup=soup, lines=lines)
        return None, None
    return product_name, price



# def returnItemInfoBulkSupplementsJson(_json, *args, **kwargs):
#     '''
#     Expects a json.loads(str)
    
#     # dict_keys(['ajaxBaseUrl', 'chooseText', 'description', 'oldPrice', 'shortDescription',
#     # 'rangeToLabel', 'productAttributes', 'productName', 'priceFromLabel', 'childProducts', 'template', 'basePrice', 
#     # 'attributes', 'showPriceRangesInOptions', 'taxConfig', 'productId'])
#     '''
#     fp = kwargs['fp']
#     name = None
#     price = None
#     items = []
#     for item in _json['attributes']['134']['options']:
#         for _id in _json['childProducts'].keys():
#                 if _id in item['products'][0]:
#                     name = item['label']
#                     price = _json['childProducts'][_id]
#                     product_id = _id # not used
#                     check_name_price(fp,name,price)
#                     items.append([name,price])
#     return items
# def returnItemInfoFromSite(fp, *args, **kwargs):
#     '''
#     [LiftMode, NewMind] uses magento
#     Magento updates its html with javascript internally and does not post
#     any dictionaries/json to the site for their items
#     '''
#     retailer = kwargs['retailer']
#     _reval = kwargs['_reval']
#     _multi = kwargs['_dict']['multi_size']
#     name = None
#     price = None

#     lines = readFile(fp)
#     soup = BS(lines)
#     # name
#     try:
#         product_name = soup.find_all("h1",itemprop="name")[0].next
#         name = product_name[0].next
#     except Exception as e:
#         pass
    # # nootropicscity uses h2 in their name
    # if len(product_name) is 0:
    #     try:
    #         product_name = 
    #         name = product_name[0].next
    #     except Exception as e:
    #         #check_error(e,fp,name=name,price=price,product_name=product_name)
    #         pass


    # ########
    # Variants
    ######
    #newstarnootropics
    #peaknootropics
    #powdercity
    #bulksupplements # handled seperately
    # if _multi is True:
    #     try:
    #         units = None
    #         unit_of_measure = None
    #         prices = None
    #         units = exec(_reval[retailer]['units']) # Units
    #         unit_of_measure = exec(_reval[retailer]['unit_of_measure']) # Unit of Measure
    #         prices = exec(_reval[retailer]['prices']) #prices  
    #         print(units, unit_of_measure, prices)
    #     except Exception as e:
    #         print(e)
    #         pass
    # # price        
    # try:
    #     # soup.find_all("table",class_="variations")[0].find_all('option')[2]['value'] # Units
    #     # soup.find_all("table",class_="variations")[0].find('label').next # Unit of Measure
    #     # soup.find_all(attrs={'class': 'entry-summary'})[0].find_all('span',class_="amount") #prices
    #     product_price = soup.find("meta",itemprop="price").attrs['content']
    #     price = product_price.attrs['content']
    # except Exception as e:
    #     #check_error(e,fp,name=name,price=price,product_name=product_name, product_price=product_price)
    #     pass

    # check_name_price(fp,name,price)
    # return name, price

# def returnItemInfoNewStar(fp):
#     '''
#     custom site with a weird dropdown menu
#     '''
#     name = None
#     price = None

#     lines = readFile(fp)
#     soup = BS(lines, 'html5lib') # malformed tags from html5 javascript use html5lib to sanitize
#     products = [product.text.split(' - ') for product in soup.find_all("option")]

#     items = []
#     for item in products:
#         name = item[0]
#         price = item[1]
#         items.append([name,price])
#         check_name_price(fp,name,price)
#     # import pdb;pdb.set_trace()
#     return items

# def returnItemInfoPowderCity(fp):
#     name = None
#     price = None

#     lines = readFile(fp)
#     soup = BS(lines)
#     name =  soup.find_all("h1", id="product-title")[0].next
#     price = soup.find_all("span", itemprop="price")[0].next
#     check_name_price(fp,name,price)
#     return name, price