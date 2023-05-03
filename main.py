import platform
from datetime import datetime, timedelta
import aiohttp
import asyncio


async def get_data(date):
    p = []
    for i in (date):
       
        async with aiohttp.ClientSession() as session:     
            async with session.get("https://api.privatbank.ua/p24api/exchange_rates?json&date=" + i) as response:

                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])
                print('Cookies: ', response.cookies)
                print(response.ok)
                
                result = await response.json()
                u = kurs(result)               
                if u != None :
                        d = {i:u}
                        p.append(d)
    return p


def dates(day):
    list = []
    current_datetime = datetime.now().date()
    for i in range(day):
        current_datetime = datetime.now().date() - timedelta(days=i)
        day =  str(current_datetime).split('-')
        day.reverse()
        date = '.'.join(day)
        list.append(date)
    return list


def kurs(data):

    list =[]
       

    if "exchangeRate" in data:
        data = data['exchangeRate']
        for i in data:
            if i['currency'] in ['EUR', 'USD']:
                currency, sale, purchase =  i['currency'],i['saleRate'],i['purchaseRate']
                d = {currency:{'sale':sale,'purchase':purchase}}
                list.append(d)
        return list
    

def main():
    day = int(input())
    date = dates(day)
    print(asyncio.run(get_data(date)))
    


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
   
