import time

import stockxApi
import website

fees = 0.12

searchApi = 'https://www.footlocker.ca/api/products/search?query=greatdeals%3Arelevance%3Aproducttype%3AShoes%3Abrand%3AJordan%3Abrand%3ANike&currentPage=&sort=relevance&pageSize=48&timestamp=4'


def runStockx(sku):
    shoeInfo = stockxApi.main(sku)
    return shoeInfo


def sort(thisSku, footsiteShoe, stockxInfo):
    price = footsiteShoe[thisSku]['price']
    sizes = footsiteShoe[thisSku]['sizes']
    name = stockxInfo['Name']
    print('')
    print(name)
    profit = False

    for i in sizes:
        try:
            stockxSizes = stockxInfo['sizes'][str(i)]
            if stockxSizes['estimatedPrice'] != None:
                estimatedPrice = float(stockxSizes['estimatedPrice'])
                payout = round((estimatedPrice * (1 - fees)), 2)
            else:
                payout = 0

            if (payout - 10) > float(price):
                profit = True
                print('Size {} is profitable with a price of {} and a payout of {}'.format(i, price, payout))
        except:
            print('Size {} not on stockx'.format(i))

    if profit == False:
        print('No good sizes')
        # else:
        #     print('Size {} is NOT profitable with a price of {} and a payout of {}'.format(i, price, payout))


def siteChoose():
    siteList = ['stockx', 'footlocker', 'champs', 'adidas']
    print('Sites Available: ', end='')
    for x in siteList:
        print('{}, '.format(x.title()), end='')
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

        if userSite == 'footlocker' or userSite == 'champs':
            skuInput = input('Please enter {} sku (x to quit): '.format(userSite))
            if skuInput == 'x':
                quit()

            print(' ')
            print('Getting info from {}... '.format(userSite))
            footsiteShoe = website.footsite(userSite, skuInput)

            print(footsiteShoe)

            # for each sku in footlocker list
            for thisSku in footsiteShoe:
                time.sleep(2)
                print('Getting Stockx info for {}...'.format(thisSku))
                stockxInfo = runStockx(thisSku)
                print(stockxInfo)

                if stockxInfo == None:
                    print('No Product')

                else:

                  sort(thisSku, footsiteShoe, stockxInfo)

        elif userSite == 'stockx':
            skuInput = input('Please enter sku (x to quit): '.format(userSite))
            if skuInput == 'x':
                quit()
            stockxInfo = runStockx(skuInput)

            name = stockxInfo['Name']
            print('')
            print('\n {}'.format(name))
            stockxSizes = stockxInfo['sizes']
            for x in stockxSizes:
                if stockxSizes[x]['estimatedPrice'] != None:
                    estimatedPrice = float(stockxSizes[x]['estimatedPrice'])
                    payout = round((estimatedPrice * (1 - fees)), 2)
                else:
                    payout = 0

                print('Size {} Payout: {}'.format(x, payout))

        elif userSite == 'adidas':

            a = input('Type go: ').lower()
            if a == 'go':
                pass
            else:
                quit()


            print(' ')
            print('Getting info from {}... '.format(userSite))
            adidasShoes = website.adidas()

            print(adidasShoes)

            # for each sku in footlocker list
            for thisSku in adidasShoes:
                print('Getting Stockx info for {}...'.format(thisSku))
                stockxInfo = runStockx(thisSku)
                print(stockxInfo)

                if stockxInfo == None:
                    print('No Product')

                else:

                    sort(thisSku, adidasShoes, stockxInfo)


        else:

            print('Not Ready Yet')


main()

