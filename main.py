from bs4 import BeautifulSoup
import requests
import time
from pushover import init, Client
import random

from config import Config

# headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

with open('user_agents.txt') as f:
    user_agents = f.read().splitlines()
    f.close()

shops = {'coolblue':{'urls':['https://www.coolblue.nl/product/865866/playstation-5.html', 
                            'https://www.coolblue.nl/product/869587/sony-playstation-5-dualsense-draadloze-controller.html']
                            }}

users = {'Myrdin':'u2peec5j2cihqg6jp2ozez5v78nr8p',
        # 'Sven':'us51jg8q6kw25hmugxgx8zp8r76nci'
}

def get_random_ua():
    random_ua = ''
    try:
        idx = random.randrange(0, len(user_agents)-1, 1)
        random_ua = user_agents[int(idx)]
    except Exception as ex:
        print('Exception in random_ua')
        print(str(ex))
    finally:
        return random_ua

def main_loop():
    while True:
        for func in shopfuncs:
            func
        time.sleep(100)

def coolblue():
    try:
        req = requests.get(shops['coolblue']['urls'][1], headers={'User-Agent':get_random_ua()})
        print("Coolblue - {} - {}".format(req.status_code, req.reason))
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("button", {"class": "js-add-to-cart-button"})
        if in_cart == None:
            print("Out of stock")
        elif in_cart != None:
            print("In stock!!")
            send_notification('Coolblue', shops['coolblue']['urls'][0])
    except:
        print("Error for Coolblue, message: {} - {}".format(req.status_code, req.reason))


def send_notification(shop, url):
    for user in users:
        print("Message to: "+user)
        client = Client(users[user],
                        api_token=Config.PUSHOVERTOKEN)
        client.send_message('PS5 beschikbaar bij {}. Click link:'.format(shop), 
                            title="PS5 in Stock!", url=url)



shopfuncs = [coolblue()]
main_loop()
# send_notification('Coolblue', shops['coolblue']['urls'][0])