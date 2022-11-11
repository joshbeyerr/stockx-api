import stockxApi
import website

sku = '53912950'
fees = 0.12

searchApi = 'https://www.footlocker.ca/api/products/search?query=greatdeals%3Arelevance%3Aproducttype%3AShoes%3Abrand%3AJordan%3Abrand%3ANike&currentPage=&sort=relevance&pageSize=48&timestamp=4'


def runStockx(sku):
    shoeInfo = stockxApi.main(sku)
    return shoeInfo


def sort(thisSku, footlockerShoe, stockxInfo):
    price = footlockerShoe[thisSku]['price']
    sizes = footlockerShoe[thisSku]['sizes']
    name = stockxInfo['Name']
    print('')
    print(name)
    profit = False

    for i in sizes:
        stockxSizes = stockxInfo['sizes'][str(i)]
        if stockxSizes['estimatedPrice'] != None:
            estimatedPrice = float(stockxSizes['estimatedPrice'])
            payout = round((estimatedPrice * (1 - fees)), 2)
        else:
            payout = 0

        if (payout - 10) > float(price):
            profit = True
            print('Size {} is profitable with a price of {} and a payout of {}'.format(i, price, payout))

    if profit == False:
        print('No profitable sizes')
        # else:
        #     print('Size {} is NOT profitable with a price of {} and a payout of {}'.format(i, price, payout))


def siteChoose():
    siteList = ['footlocker']
    print('Sites Available: ', end='')
    for x in siteList:
        print(x.title(), end='')
    print('')

    siteSelect = False
    while not siteSelect:
        userSite = input('Please choose a site (x to quit): ').lower()
        if userSite in siteList:
            return userSite

        elif userSite == 'x':
            quit()

        else:
            print('Invalid Site Try Again')


def main():
    userSite = siteChoose()

    runSku = False
    while not runSku:

        if userSite == 'footlocker':
            skuInput = input('Please enter footlocker sku (x to quit): ')
            if skuInput == 'x':
                quit()

            print(' ')
            print('Getting info from footlocker... ')
            footlockerShoe = website.footlocker(skuInput)

            print(footlockerShoe)

            # for each sku in footlocker list
            for thisSku in footlockerShoe:
                print('Getting Stockx info for {}...'.format(thisSku))
                stockxInfo = runStockx(thisSku)
                print(stockxInfo)

                if stockxInfo == None:
                    print('No Product')

                else:

                    sort(thisSku, footlockerShoe, stockxInfo)

        else:
            print('Not Ready Yet')


main()
