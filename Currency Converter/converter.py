import requests


def converter():
    '''
    This is the simple program that receives from the user some code of currency he has and
    then asks about currency he needs. Exchange rate takes from the portal FloatRates using requests
    library.
    While endless cycle program offers to exchange available currency for any available according data 
    from FloatRates. It finishes after leaving a blank reply. 
    :return:
    '''
    avl_currency = input("Please input the currency, you have:\n").lower()
    cache_curr = ['usd', 'eur']
    cache_dict = {}
    for i in cache_curr:
        ip_rate = "http://www.floatrates.com/daily/" + i + ".json"
        r = requests.get(ip_rate.lower()).json()
        cache_dict[i] = r
    while True:
        need_currency = input("Now input the curr you need (leave the blank to exit):\n").lower()
        if need_currency == '':
            break
        avl_sum = int(input(f"What amount of {avl_currency} do you have?\n"))
        print('Checking the cache...')
        if need_currency in cache_dict.keys():
            print('Oh! It is in the cache!')
            amount = round(avl_sum * cache_dict[need_currency][avl_currency]['inverseRate'], 2)
            print(f'You received {amount} {need_currency.upper()}')
        else:
            print('Sorry, but it is not in the cache!')
            new_rate = "http://www.floatrates.com/daily/" + need_currency + ".json"
            r2 = requests.get(new_rate.lower()).json()
            cache_dict[need_currency] = r2
            amount = round(avl_sum * r2[avl_currency]['inverseRate'], 2)
            print(f'You received {amount} {need_currency.upper()}')


if __name__ == '__main__':
    converter()
    
