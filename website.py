import requests

sale = True

def footlocker(sku):
    shoe = {}

    s = requests.session()
    s.headers.update({
        'authority': 'footlocker.ca',

        'origin': 'https://www.footlocker.ca/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                      'Safari/537.36',

    })

    sizesAvai = []

    getShoe = s.get('https://www.footlocker.ca/zgw/product-core/v1/pdp/sku/{}'.format(sku))
    getShoe = getShoe.json()

    supplierSku = getShoe['style']['vendorAttributes']['supplierSkus'][0]
    price = float(getShoe['style']['price']['salePrice'])
    availability = getShoe['inventory']['inventoryAvailable']

    gender = getShoe['model']['genders'][0]
    if 'boys' in gender.lower() or 'girls' in gender.lower():
        tax = 1.05
    else:
        tax = 1.13

    price = round((price*tax), 2)

    if availability:
        for x in getShoe['sizes']:
            if x['inventory']['inventoryAvailable']:
                size = x['size']
                if str(size[0]) == '0':
                    size = size.lstrip(size[0])
                if '.0' in size:
                    size = size[:len(size) - 2]

                sizesAvai.append(size)

    if sale == True:
        price = round((price*0.8), 2)

    shoe[supplierSku] = {'price': price, 'sizes': sizesAvai}

    return shoe
