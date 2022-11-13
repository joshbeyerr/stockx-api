import json
import requests

s = requests.session()

s.headers.update({
    'authority': 'stockx.com',

    'origin': 'https://stockx.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                  'Safari/537.36',

})


def calculateWorth(priceInfo):
    if priceInfo['salesNumber'] <= 0:
        volume = None
    elif 1 <= priceInfo['salesNumber'] < 5:
        volume = 'low'
    elif 5 <= priceInfo['salesNumber'] < 15:
        volume = 'medium'
    elif 15 <= priceInfo['salesNumber'] < 35:
        volume = 'high'
    elif priceInfo['salesNumber'] >= 35:
        volume = 'extreme'

    else:
        volume = priceInfo['salesNumber']

    if (priceInfo['lastSale'] - 30) > priceInfo['lowestAsk']:
        estimatedPrice = round(((priceInfo['lowestAsk'] + priceInfo['highestBid']) / 2), 2)

    elif (((priceInfo['lowestAsk'] + priceInfo['lastSale'])/2) / 1.6) > priceInfo['highestBid']:
        estimatedPrice = round(((priceInfo['lowestAsk'] + priceInfo['lastSale']) / 2), 2)

    elif priceInfo['lowestAsk'] != 0 and priceInfo['highestBid'] != 0 and priceInfo['lastSale'] != 0:
        trio = round(((priceInfo['lowestAsk'] + priceInfo['highestBid'] + priceInfo['lastSale']) / 3), 2)
        duo = round(((priceInfo['lowestAsk'] + priceInfo['highestBid']) / 2), 2)
        estimatedPrice = round(((duo + trio) / 2), 2)

    elif priceInfo['lowestAsk'] != 0 and priceInfo['highestBid'] != 0:
        estimatedPrice = round(((priceInfo['lowestAsk'] + priceInfo['highestBid']) / 2), 2)
    else:
        estimatedPrice = None

    return volume, estimatedPrice


def sortJson(allInfo):
    shoe = {}

    jsoning = allInfo.json()

    # jsoning = allInfo
    styleID = jsoning['Product']['styleId']
    name = jsoning['Product']['title']
    shoe['Name'] = name
    shoe['SKU'] = styleID

    imageLin = jsoning['Product']['media']['imageUrl']
    shoe['image'] = imageLin

    sizes = {}

    for x in jsoning['Product']['children']:
        priceInfo = {}

        infoSize = jsoning['Product']['children'][x]
        marketInfo = infoSize['market']

        shoeSize = infoSize['shoeSize']
        if 'Y' in shoeSize:
            shoeSize = shoeSize.replace('Y', '')
        if 'W' in shoeSize:
            shoeSize = shoeSize.replace('W', '')

        salesN = marketInfo['salesThisPeriod']
        priceInfo['salesNumber'] = salesN

        lowestAsk = marketInfo['lowestAsk']
        priceInfo['lowestAsk'] = lowestAsk

        highestBid = marketInfo['highestBid']
        priceInfo['highestBid'] = highestBid

        lastSale = marketInfo['lastSale']
        priceInfo['lastSale'] = lastSale

        worth = calculateWorth(priceInfo)

        volume = worth[0]
        estimatedPrice = worth[1]
        priceInfo['volume'] = volume
        priceInfo['estimatedPrice'] = estimatedPrice

        if estimatedPrice is not None:
            priceInfo['probBetterEstimatedPrice'] = round((int((marketInfo['lowestAskFloat']) + estimatedPrice) / 2), 2)
        else:
            priceInfo['probBetterEstimatedPrice'] = round(int(marketInfo['lowestAskFloat']), 2)

        sizes[shoeSize] = priceInfo

    shoe['sizes'] = sizes

    return shoe


def search(sku):
    bb = s.get('https://stockx.com/api/browse?_search={}'.format(sku))
    cc = bb.json()

    for x in cc['Products']:
        styleId = str(x['styleId']).upper()
        if '-' in styleId:
            styleId = styleId.replace('-', '')

        if styleId == sku.upper():
            key = x['urlKey']
            return key


def main(sku):
    sku = sku.replace('-', '')

    urlKey = search(sku)

    if urlKey is not None:
        try:
            a = s.get(
                'https://stockx.com/api/products/{}?includes=market&variants&currency=CAD&market=CA'.format(urlKey))

        except:
            print('Error')
            quit()
        bbb = sortJson(a)

        return bbb
    else:
        print("Couldn't find product")
