import time

import requests

sale = True


def footsite(userSite, sku):
    print(userSite)
    if userSite == 'footlocker':
        link = 'https://www.footlocker.ca/'
    elif userSite == 'champs':
        link = 'https://www.champssports.ca/'

    auth = (link.split('.'))[1]
    auth = auth + '.ca'
    print(auth)

    shoe = {}

    s = requests.session()
    s.headers.update({
        'authority': auth,

        'origin': '{}'.format(link),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                      'Safari/537.36',

    })

    sizesAvai = []

    getShoe = s.get('{}zgw/product-core/v1/pdp/sku/{}'.format(link, sku))
    getShoe = getShoe.json()

    supplierSku = getShoe['style']['vendorAttributes']['supplierSkus'][0]
    price = float(getShoe['style']['price']['salePrice'])
    availability = getShoe['inventory']['inventoryAvailable']

    gender = getShoe['model']['genders'][0]
    if 'boys' in gender.lower() or 'girls' in gender.lower():
        tax = 1.05
    else:
        tax = 1.13

    price = round((price * tax), 2)

    if availability:
        for x in getShoe['sizes']:
            if x['inventory']['inventoryAvailable']:
                size = x['size']
                if str(size[0]) == '0':
                    size = size.lstrip(size[0])
                if '.0' in size:
                    size = size[:len(size) - 2]

                sizesAvai.append(size)

    if sale:
        price = round((price * 0.8), 2)

    shoe[supplierSku] = {'price': price, 'sizes': sizesAvai}

    return shoe

def adidas():

    shoes = {}

    limit = 2
    s = requests.session()
    s.headers.update({
        'authority': 'www.adidas.ca',

        'referer': 'https://www.adidas.ca/en',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                      'Safari/537.36',

    })
    #adidasInf = (s.get('https://www.adidas.ca/api/plp/content-engine/search?sitePath=en&query=samba')).json()
    adidasInf = (s.get('https://www.adidas.ca/api/plp/content-engine?sitePath=en&query=men-athletic_sneakers-shoes-outlet&start=48')).json()

    items = adidasInf['raw']['itemList']['items']

    count = 0
    for x in items:

        print(count)

        if count == limit:
            print(shoes)
            return shoes
        supplierSku = x['productId']
        print(supplierSku)
        price = x['salePrice']
        specific = (s.get('https://www.adidas.ca/api/products/{}/availability?sitePath=en'.format(supplierSku))).json()
        if specific['availability_status'] == 'IN_STOCK':
            sizesAvai = []
            for i in specific['variation_list']:
                if i['availability_status'] == 'IN_STOCK':
                    size = i['size']
                    if '/' in size:
                        size = size.split('/')
                        size = size[0].strip('M ')
                    sizesAvai.append(size)



            shoes[supplierSku] = {'price': price, 'sizes': sizesAvai}
            count += 1

    return shoes


def nike():
    pass

def shopify():
    pass

def sportchek():
    pass

def ssense():
    pass

