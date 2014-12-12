import os, json
from bs4 import BeautifulSoup as BS

log = open('log','a+')

def readFile(fp):
    # if the file is zero length the url fetcher failed
    if os.stat(fp).st_size is 0:
        raise Exception("[ERROR] File zero length",fp)
    with open(fp,'r') as f:
        lines = f.read()
    return lines


def returnJsonFromBulkSupplements(fp, leadsplit, endsplit):
    try:
        lines = readFile(fp)
    except:
        import traceback;log.write(traceback.format_exc())
        log.write(fp+"\n")
        return None
    _json = lines.split(leadsplit)[1].split(endsplit)[0]
    _json = json.loads(_json)
    return _json
    
def returnJsonFromJsonDumpFile(fp):
    try:
        _json= readFile(fp)
    except:
        import traceback;log.write(traceback.format_exc())
        log.write(fp+"\n")
        return None
    _json = json.loads(_json)
    return _json

def returnItemInfoBulkSupplementsJson(_json):
    '''
    Expects a json.loads(str)
    
    # dict_keys(['ajaxBaseUrl', 'chooseText', 'description', 'oldPrice', 'shortDescription',
    # 'rangeToLabel', 'productAttributes', 'productName', 'priceFromLabel', 'childProducts', 'template', 'basePrice', 
    # 'attributes', 'showPriceRangesInOptions', 'taxConfig', 'productId'])
    '''
    for item in _json['attributes']['134']['options']:
        for _id in _json['childProducts'].keys():
                if _id in item['products'][0]:
                    name = item['label']
                    price = _json['childProducts'][_id]
                    product_id = _id # not used
                    print('Parsed bulk supplements: ','\n',name, price)
    return
    
def returnItemInfoFromHRNDJson(_json):
    '''
    print(_json.keys())
    print(_json['details'].keys())
    dict_keys(['details', 'success'])
    dict_keys(['sku', 'thumb', 'purchasable', 'baseThumb', 'unformattedPrice', 'unformattedRrp', 'upc', 'priceLabel', 'price', 'base', 'instock', 'baseImage', 'image', 'rrp'])
    '''
    # name(based on picture name in thumb image), price
    if _json is None:
        return
    name = _json['details']['thumb'].split('/')[-1].split('.')[0].split('__')[0]
    price = _json['details']['price']
    print('Parsed','\n',name, price)
    return name,price

def returnItemInfoFromMagentoSite(fp):
    '''
    [LiftMode, NewMind] uses magento
    Magento updates its html with javascript internally and does not post
    any dictionaries/json to the site for their items
    '''
    lines = readFile(fp)
    soup = BS(lines)
    
    try:
        product_name = soup.find_all("h1",itemprop="name")
        name = product_name[0].next
    except Exception as e:
        pass
    # nootropicscity uses h2 in their name
    if len(product_name) is 0:
        try:
            #if fp in '/home/bob/documents/p_city_prices/nootropicscity/Phenylpiracetam':
                #import pdb;pdb.set_trace()
            product_name = soup.find_all("h2",itemprop="name")
            name = product_name[0].next
        except Exception as e:
            import traceback;log.write(traceback.format_exc())
            log.write(fp+"\n")
            pass
    try:
        product_price = soup.find("meta",itemprop="price")
        price = product_price.attrs['content']
    except Exception as e:
        import traceback;log.write(traceback.format_exc())
        log.write(fp+"\n")
        pass

    print('Parsed',fp,'\n',name, price)
    return name, price

def returnItemInfoNewStar(fp):
    '''
    custom site with a weird dropdown menu
    '''
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
        print('Parsed',fp,'\n',name, price)
    return items

def returnItemInfoPowderCity(fp):
    lines = readFile(fp)
    soup = BS(lines)
    name =  soup.find_all("h1", id="product-title")[0].next
    price = soup.find_all("span", itemprop="price")[0].next
    print('Parsed',fp,'\n',name, price)
    return name, price

