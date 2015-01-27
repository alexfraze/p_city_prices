# -*- coding: utf-8 -*-
import json
import os
import shopify
import time
from operator import itemgetter, attrgetter

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_SHOPNAME = os.environ['API_SHOPNAME']

shop_url = "https://{0}:{1}@{2}.myshopify.com/admin".format(os.environ['API_KEY'], os.environ['API_SECRET'], os.environ['API_SHOPNAME'])
shopify.ShopifyResource.set_site(shop_url)

def pageCount(count, limit):
    '''
    return ceiling
    '''
    return int(-(-count // float(limit)))

def getAllProductDict():
    limit = 250
    product_count = shopify.Product.count()
    page_count = pageCount(product_count, limit)
    products = {}
    for _p in range(1, page_count):
        _list = shopify.Product.find(page=_p, limit=limit)
        for product in _list:
            products.update({product.to_dict()['id']:product.to_dict()})
        time.sleep(.5)
    return products

def go_pdb(item):
    print(item)
    import pdb;pdb.set_trace()
    return

def p_d(item, _len):
    for key in item.keys():
        print('    '*_len+"{0}: {1}".format(key, item[key]))
        if type(item[key]) is dict:
            p_d(item[key], _len+1)
    return

def check_key(item, key):
    try:
        if len(item[key]) > 0:
            return True
        else:
            return False
    except:
        return False

def returnEstimate(item):
    '''asdf
    '''
    p = item['scraped']['scraped_price']
    d = [' ', '$']
    for k in d:
        p = p.replace(k, '')
    p = float(p)
    
    total_units = float(item['csv_info']['total_units'])
    return p/total_units

def inputChoice(item):
    choices = {'pdb': 'go_pdb(item)', 
               'p':'p_d(item, 1)', 
               '0':'results_wrong.append(item)', 
               '': "ok=True;results_okay.append(item);print(ok)"
               }
    ok = False
    while ok is False:
        r = input("Input: ")
        try:
           ok = exec(choices[r])
        except Exception as e:
            print(e)
            print("I didn't understand.")
            print("Choices")
            for key in choices.keys():
                _key = key
                if key == '':
                    _key = "[enter]"
                print('    {0} : {1}'.format(_key, choices[key]))
    return

def guessAndUpdateUnits(item):
    if len(item['scraped']['smulti_prices']) is len(item['scraped']['scraped_units']):
        new = []
        for i in item['scraped']['scraped_units']:
            if i[0] is ' ':
                i = i[1:]
            if '¼' in i:
                i = i.replace(' ¼', '.25 ').replace('¼ ', '.25 ').replace('¼', '.25 ')
            if '½' in i:
                i = i.replace(' ½', '.5').replace(' ½ ', '.5').replace('½', '.5')
            if ' gram ' in i:
                i = i.split(' gram ')
            elif ' grams ' in i:
                i = i.split(' grams ')
            new.append(float(i[0]))
        item['scraped']['scraped_units'] = sorted(new)

def cleanMultiPrices(item):
    new = []
    for p in item['scraped']['smulti_prices']:
        p = p.replace(' ', '').replace(' ', '').replace('$', '')
        new.append(float(p))
    item['scraped']['smulti_prices'] = sorted(new)

def checkInternalSku(_it):
    _it = item['csv_info']['internal_sku']
    
    for x in price_chart:
        for y in x:
            #print(y)
            if _it in y:
                return True
    return False        

def run(items, *args, **kwargs):
    results_okay = []
    results_wrong = []
    _file = './current_products.json'
    if os.path.exists(_f):
        s = (time.time() - os.stat(_file).st_mtime ) / 60 
    else:
        current_products = getAllProductDict()
        with open(_file,'w+') as f:
            json.dump(current_products,f)
        s = (time.time() - os.stat(_file).st_mtime ) / 60 

    try:
        if s < 30:
            with open(_file, 'r') as f:
                current_products = json.load(f)
        else:
            current_products = getAllProductDict()
            with open(_file,'w+') as f:
                json.dump(current_products,f)
    except Exception as e:
        import traceback;print(traceback.format_exc())
        print(e)
        exit()
        pass
    price_chart = []
    # .sort(key=lambda x: x[2])
    for p in current_products.keys():
        x = [[x['sku'].split('-')[0],x['sku'],x['grams'],x['price'],p] for x in current_products[p]['variants']]
        x = sorted(x, key=itemgetter(2))
        price_chart.append(x)
    for item in items:
        _it = item['csv_info']['internal_sku']
        sku_exists = checkInternalSku(_it)
        if sku_exists:
            if check_key(item['scraped'], 'scraped_units'):
                print('\n'+item['csv_info']['internal_sku'])
                guessAndUpdateUnits(item)
                cleanMultiPrices(item)
                if len(item['scraped']['smulti_prices']) is len(item['scraped']['scraped_units']):
                    for i, x in enumerate(item['scraped']['smulti_prices']):
                        print(float(item['scraped']['smulti_prices'][i])/float(item['scraped']['scraped_units'][i]))
                else:
                    results_wrong.append(item)
                pass
            elif check_key(item['scraped'], 'scraped_price'):
                print('\n'+item['csv_info']['internal_sku'])
                print(returnEstimate(item))
                p_d(item, 1)
                pass

    print(results_wrong)

    #inputChoice(item)


# with open('okay', 'w+') as f:
#     import json
#     json.dump(results_okay, f)
# with open('wrong', 'w+') as f:
#     import json
#     json.dump(results_wrong, f)
# import pdb;pdb.set_trace()

# (Pdb) import pickle
# (Pdb) pickle.dump(results_okay, open('okay.p', 'wb'))
# (Pdb) pickle.dump(results_wrong, open('wrong.p', 'wb'))
if __name__ == "__main__":
    with open('parsed', 'r+') as f:
        items = json.load(f)
    print(len(items))
    exit()
    run(items, './products1.json', './products2.json', './products3.json')
