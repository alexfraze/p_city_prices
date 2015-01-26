import json

def go_pdb(item):
    print(item)
    import pdb;pdb.set_trace()
    return

def p_d(item, _len):
    for key in item.keys():
        print('    '*_len+"{0}: {1}".format(key,item[key]))
        if type(item[key]) is dict:
            p_d(item[key],_len+1)
    return

def check_key(item,key):
    try:
        if len(item[key]) > 0:
            return True
        else:
            return False
    except:
        return False
def returnEstimate(item):
    p = item['scraped']['scraped_price']
    _d = [' ','$']
    for k in _d:
        p = p.replace(k,'')
    p = float(p)
    
    total_units = float(item['csv_info']['total_units'])
    return p/total_units

def inputChoice(item):
    choices = {'pdb': 'go_pdb(item)',
               'p':'p_d(item,1)',
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
                print('    {0} : {1}'.format(_key,choices[key]))
    return

def guessAndUpdateUnits(item):
    if len(item['scraped']['smulti_prices']) is len(item['scraped']['scraped_units']):
        new = []
        for i in item['scraped']['scraped_units']:
            if i[0] is ' ':
                i = i[1:]
            if '¼' in i:
                i = i.replace(' ¼','.25 ').replace('¼ ','.25 ').replace('¼','.25 ')
            if '½' in i:
                i = i.replace(' ½','.5').replace(' ½ ','.5').replace('½','.5')
            if ' gram ' in i:
                i = i.split(' gram ')
            elif ' grams ' in i:
                i = i.split(' grams ')
            new.append(float(i[0]))
        item['scraped']['scraped_units'] = sorted(new)

def cleanMultiPrices(item):
    new = []
    for p in item['scraped']['smulti_prices']:
        p = p.replace(' ','').replace(' ','').replace('$','')
        new.append(float(p))
    item['scraped']['smulti_prices'] = sorted(new)

        

def run(items,*args, **kwargs):
    results_okay = []
    results_wrong = []
    print(args[0])
    with open(args[0],'r') as f:
        a = json.load(f)

    import pdb;pdb.set_trace()
    for item in items:
        #print("Do these units match?")
        if check_key(item['scraped'],'scraped_units'):
            print('\n'+item['csv_info']['internal_sku'])
            guessAndUpdateUnits(item)
            cleanMultiPrices(item)
            if len(item['scraped']['smulti_prices']) is len(item['scraped']['scraped_units']):
                for i, x in enumerate(item['scraped']['smulti_prices']):
                    print(float(item['scraped']['smulti_prices'][i])/float(item['scraped']['scraped_units'][i]))
            p_d(item['scraped'],1)
            continue
        elif check_key(item['scraped'],'scraped_price'):
            #print('\n'+item['csv_info']['internal_sku'])
            #print(returnEstimate(item))
            #p_d(item,1)
            pass

    #inputChoice(item)


# with open('okay','w+') as f:
#     import json
#     json.dump(results_okay,f)
# with open('wrong','w+') as f:
#     import json
#     json.dump(results_wrong,f)
# import pdb;pdb.set_trace()

# (Pdb) import pickle
# (Pdb) pickle.dump(results_okay, open('okay.p', 'wb'))
# (Pdb) pickle.dump(results_wrong, open('wrong.p', 'wb'))
if __name__ == "__main__":
    with open('parsed','r+') as f:
        items = json.load(f)
    run(items,'./products1.json','./products2.json','./products3.json')
