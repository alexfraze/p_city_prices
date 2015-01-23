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

def returnItemInfoBulkSupplementsJson(_json, *args, **kwargs):
    '''
    Expects a json.loads(str)
    
    # dict_keys(['ajaxBaseUrl', 'chooseText', 'description', 'oldPrice', 'shortDescription',
    # 'rangeToLabel', 'productAttributes', 'productName', 'priceFromLabel', 'childProducts', 'template', 'basePrice', 
    # 'attributes', 'showPriceRangesInOptions', 'taxConfig', 'productId'])
    '''
    fp = kwargs['fp']
    name = None
    price = None
    items = []
    for item in _json['attributes']['134']['options']:
        for _id in _json['childProducts'].keys():
                if _id in item['products'][0]:
                    name = item['label']
                    price = _json['childProducts'][_id]
                    product_id = _id # not used
                    check_name_price(fp,name,price)
                    items.append([name,price])
    return items
    
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

def returnItemInfoFromMagentoSite(fp, *args, **kwargs):
    '''
    [LiftMode, NewMind] uses magento
    Magento updates its html with javascript internally and does not post
    any dictionaries/json to the site for their items
    '''
    retailer = kwargs['retailer']
    _multi = kwargs['_dict']['multi_size']
    name = None
    price = None

    lines = readFile(fp)
    soup = BS(lines)
    # name
    try:
        product_name = soup.find_all("h1",itemprop="name")
        name = product_name[0].next
    except Exception as e:
        pass
    # nootropicscity uses h2 in their name
    if len(product_name) is 0:
        try:
            product_name = soup.find_all("h2",itemprop="name")
            name = product_name[0].next
        except Exception as e:
            #check_error(e,fp,name=name,price=price,product_name=product_name)
            pass


    # ########
    # Variants
    ######
    #newstarnootropics
    #peaknootropics
    #powdercity
    #bulksupplements # handled seperately
    if _multi is True:
        _reval = {'peaknootropics': {'units':'[x["value"] for x in soup.find_all("table",class_="variations")[0].find_all("option")]',
                                     'unit_of_measure': 'soup.find_all("table",class_="variations")[0].find("label").next',
                                     'prices': 'soup.find_all(attrs={"class": "entry-summary"})[0].find_all("span",class_="amount")'
                                    },
                  # 'liftmode': {'units': 'import pdb;pdb.set_trace()',
                  #              'unit_of_measure': '',
                  #              'prices': ''
                  #             },
                  # 'liftmode': {'units': 'import pdb;pdb.set_trace()',
                  #              'unit_of_measure': '',
                  #              'prices': ''
                  #             },
                  # 'liftmode': {'units': 'import pdb;pdb.set_trace()',
                  #              'unit_of_measure': '',
                  #              'prices': ''
                  #             },
                  # 'liftmode': {'units': 'import pdb;pdb.set_trace()',
                  #              'unit_of_measure': '',
                  #              'prices': ''
                  #             },

                 }
        try:
            units = None
            unit_of_measure = None
            prices = None
            units = exec(_reval[retailer]['units']) # Units
            unit_of_measure = exec(_reval[retailer]['unit_of_measure']) # Unit of Measure
            prices = exec(_reval[retailer]['prices']) #prices  
            print(units, unit_of_measure, prices)
        except Exception as e:
            print(e)
            pass
    # price        
    try:
        # soup.find_all("table",class_="variations")[0].find_all('option')[2]['value'] # Units
        # soup.find_all("table",class_="variations")[0].find('label').next # Unit of Measure
        # soup.find_all(attrs={'class': 'entry-summary'})[0].find_all('span',class_="amount") #prices
        product_price = soup.find("meta",itemprop="price")
        price = product_price.attrs['content']
    except Exception as e:
        #check_error(e,fp,name=name,price=price,product_name=product_name, product_price=product_price)
        pass

    check_name_price(fp,name,price)
    return name, price

def returnItemInfoNewStar(fp):
    '''
    custom site with a weird dropdown menu
    '''
    name = None
    price = None

    lines = readFile(fp)
    soup = BS(lines, 'html5lib') # malformed tags from html5 javascript use html5lib to sanitize
    products = soup.find_all("option")
    products = [ product.text for product in products ]
    products = [product.split(' - ') for product in products]
    items = []
    for item in products:
        name = item[0]
        price = item[1]
        items.append([name,price])
        check_name_price(fp,name,price)
    return items

def returnItemInfoPowderCity(fp):
    name = None
    price = None

    lines = readFile(fp)
    soup = BS(lines)
    name =  soup.find_all("h1", id="product-title")[0].next
    price = soup.find_all("span", itemprop="price")[0].next
    check_name_price(fp,name,price)
    return name, price

def check_error( e, fp, *args, **kwargs):
    import pdb;pdb.set_trace()

    return


def check_name_price(fp, name, price):
    # check
    try:
        if (name is None) and (price is None):
            error = 'ITEM MISSING: {0}'.format(fp)
            print(error)
            log.write(error+'\n')
        elif (name is None):
            error = 'NAME MISSING: {0}'.format(fp)
            print(error)
            log.write(error+'\n')            
        elif (price is None):
            error = 'Price MISSING: {0}'.format(fp)
            print(error)
            log.write(error+'\n')        
        else:
            print('Parsed',fp,'\n',name, price)
            return
    except:
        import pdb;pdb.set_trace()
    return    