from bs4 import BeautifulSoup
import requests
import time
from pushover import init, Client
import random

from config import Config

with open('user_agents.txt') as f:
    user_agents = f.read().splitlines()
    f.close()

shops = {'coolblue':{'urls':['https://www.coolblue.nl/product/865866/playstation-5.html', 
                            'https://www.coolblue.nl/product/869587/sony-playstation-5-dualsense-draadloze-controller.html']
        },
        'amazonde':{'urls':['https://www.amazon.de/PS5-Konsole-Sony-PlayStation-Standard/dp/B08VLX84G6/',
                            'https://www.amazon.de/Sony-DualSense-Wireless-Controller-PlayStation-5/dp/B08H93ZRK9/']
        },
        'amazonnl':{'urls':['https://www.amazon.nl/Sony-PlayStation-PlayStation®5-Console/dp/B08H93ZRK9',
                            'https://www.amazon.nl/Sony-PlayStation-9399506-PlayStation®5-Controller/dp/B08H97WTBL/'],
        }
}


users = {'Myrdin':'u2peec5j2cihqg6jp2ozez5v78nr8p',
         'Sven':'us51jg8q6kw25hmugxgx8zp8r76nci'
}

def get_random_ua():
    random_ua = ''
    try:
        idx = random.randrange(0, len(user_agents)-1, 1)
        random_ua = user_agents[int(idx)]
    except Exception as ex:
        print('Exception in random_ua', flush=True)
        print(str(ex))
    finally:
        return random_ua

def main_loop():
    while True:
        coolblue()
        amazonde()
        amazonnl()
        time.sleep(120)

def coolblue():
    try:
        req = requests.get(shops['coolblue']['urls'][0], headers={'User-Agent':get_random_ua()})
        print("Coolblue - {} - {}".format(req.status_code, req.reason), flush=True)
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("button", {"class": "js-add-to-cart-button"})
        if in_cart == None:
            print("Out of stock", flush=True)
        elif in_cart != None:
            print("In stock!!", flush=True)
            send_notification('Coolblue', shops['coolblue']['urls'][0])
    except:
        print("Error for Coolblue, message: {} - {}".format(req.status_code, req.reason))


def amazonde():
    try:
        req = requests.get(shops['amazonde']['urls'][0], headers={'User-Agent':get_random_ua()})
        print("Coolblue - {} - {}".format(req.status_code, req.reason))
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("input", {"id": "add-to-cart-button"})
        if in_cart == None:
            print("Out of stock")
        elif in_cart != None:
            print("In stock!!")
            send_notification('Amazon DE', shops['amazonde']['urls'][0])
    except:
        print("Error for Amazon DE, message: {} - {}".format(req.status_code, req.reason))


def amazonnl():
    try:
        req = requests.get(shops['amazonnl']['urls'][0], headers={'User-Agent':get_random_ua()})
        print("Coolblue - {} - {}".format(req.status_code, req.reason))
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("input", {"id": "add-to-cart-button"})
        if in_cart == None:
            print("Out of stock")
        elif in_cart != None:
            print("In stock!!")
            send_notification('Amazon NL', shops['amazonnl']['urls'][0])
    except:
        print("Error for Amazon NL, message: {} - {}".format(req.status_code, req.reason))



def send_notification(shop, url):
    for user in users:
        print("Message to: "+user, flush=True)
        client = Client(users[user],
                        api_token=Config.PUSHOVERTOKEN)
        client.send_message('PS5 beschikbaar bij {}. Click link:'.format(shop), 
                            title="PS5 in Stock!", url=url)



if __name__ == '__main__':
    main_loop()
