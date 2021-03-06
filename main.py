from bs4 import BeautifulSoup
import requests
import time
from pushover import init, Client
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import Config

with open('user_agents.txt') as f:
    user_agents = f.read().splitlines()
    f.close()

shops = {'coolblue': {'urls': ['https://www.coolblue.nl/product/865866/playstation-5.html',
                               'https://www.coolblue.nl/product/869587/sony-playstation-5-dualsense-draadloze-controller.html']
                      },
         'amazonde': {'urls': ['https://www.amazon.de/PS5-Konsole-Sony-PlayStation-Standard/dp/B08VLX84G6/',
                               'https://www.amazon.de/Sony-DualSense-Wireless-Controller-PlayStation-5/dp/B08H93ZRK9/']
                      },
         'amazonnl': {'urls': ['https://www.amazon.nl/Sony-PlayStation-PlayStation®5-Console/dp/B08H93ZRK9',
                               'https://www.amazon.nl/Sony-PlayStation-9399506-PlayStation®5-Controller/dp/B08H97WTBL/'],
                      },
         'nedgame': {'urls': ['https://www.nedgame.nl/playstation-5/playstation-5-disc-version-bundel/9820628451/',
                              'https://www.nedgame.nl/playstation-5/sony-dualsense-wireless-controller/6022334263/'],
                     },
         'nedgame2': {'urls': ['https://www.nedgame.nl/playstation-5/playstation-5-digital-edition-bundel/6481373393',
                               'https://www.nedgame.nl/playstation-5/sony-dualsense-wireless-controller/6022334263/'],
                      },
         'mediamarkt': {'urls': ['https://www.mediamarkt.nl/nl/product/_sony-playstation-5-disk-edition-1664768.html',
                                 'https://www.mediamarkt.nl/nl/product/_sony-playstation-5-dualsense-wit-1664770.html'],
                        },
         'bol': {'urls': ['https://www.bol.com/nl/p/sony-playstation-5-console/9300000004162282/',
                          'https://www.bol.com/nl/p/sony-ps5-dualsense-draadloze-controller/9300000007897748/']
                 },
         'gamemania': {'urls': ['https://www.gamemania.nl/Consoles/playstation-5/144093_playstation-5-disc-edition',
                                'https://www.gamemania.nl/Accessories/controllers/145722_playstation-5-dualsense-draadloze-controller']
                       }
         }

users = {
    # 'Myrdin': 'u2peec5j2cihqg6jp2ozez5v78nr8p',
    #  'Sven': 'us51jg8q6kw25hmugxgx8zp8r76nci',
    #  'Davy': 'uznan927os8jwo22bbwidroo5xa9xw',
    'Sjors': 'ugsgjkwm4gj7h7ay8pgtgpiqusjzo8'

}

send_to_email = ["m.vanderhorst@districon.com",
                 "Sjorsvanroos@hotmail.com"
                 ]

referers = [
    'http://www.bing.com/',
    'http://www.google.com/',
    'https://search.yahoo.com/',
    'http://www.baidu.com/',
    'https://duckduckgo.com/'
]

prod = 0


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
        # amazonnl()
        nedgame()
        nedgame2()
        mediamarkt()
        bol()
        gamemania()
        time.sleep(random.randrange(20, 60, 1))


def coolblue():
    try:
        req = requests.get(shops['coolblue']['urls'][prod], headers={
                           'User-Agent': get_random_ua(), 'referer': random.choice(referers)})
        print("Coolblue - {} - {}".format(req.status_code, req.reason), flush=True)
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("button", {"class": "js-add-to-cart-button"})
        if in_cart == None:
            print("Out of stock", flush=True)
        elif in_cart != None:
            print("In stock!!", flush=True)
            send_notification('Coolblue', shops['coolblue']['urls'][prod])
    except Exception as ex:
        print('Exception in coolblue', flush=True)
        print(str(ex))


def amazonde():
    try:
        req = requests.get(shops['amazonde']['urls'][prod], headers={
                           'User-Agent': get_random_ua(), 'referer': random.choice(referers)})
        print("Amazon DE - {} - {}".format(req.status_code, req.reason))
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("input", {"id": "add-to-cart-button"})
        if in_cart == None:
            print("Out of stock")
        elif in_cart != None:
            print("In stock!!")
            send_notification('Amazon DE', shops['amazonde']['urls'][prod])
    except Exception as ex:
        print('Exception in Amazon DE', flush=True)
        print(str(ex))


def amazonnl():
    try:
        req = requests.get(shops['amazonnl']['urls'][prod], headers={
                           'User-Agent': get_random_ua(), 'referer': random.choice(referers)})
        print("Amazon NL - {} - {}".format(req.status_code, req.reason))
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("input", {"id": "add-to-cart-button"})
        if in_cart == None:
            print("Out of stock")
        elif in_cart != None:
            print("In stock!!")
            send_notification('Amazon NL', shops['amazonnl']['urls'][prod])
    except Exception as ex:
        print('Exception in Amazon NL', flush=True)
        print(str(ex))


def mediamarkt():
    try:
        store = ['mediamarkt', 'Media Markt']
        req = requests.get(shops[store[0]]['urls'][prod], headers={
                           'User-Agent': get_random_ua(), 'referer': random.choice(referers)})
        print("{} - {} - {}".format(store[1], req.status_code, req.reason))
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("div", {"class": "box infobox availability"})
        try:
            in_cart_text = in_cart.text.replace(" ", "").lower()
        except:
            in_cart_text = ''
        print(in_cart_text)
        if "uitverkocht" in in_cart_text or in_cart_text == '':
            print("Out of stock")
        elif soup.find("a", {"id": "pdp-add-to-cart"}) != None:
            print("In stock!!")
            send_notification(store[1], shops[store[0]]['urls'][prod])
    except Exception as ex:
        print('Exception in Media Markt', flush=True)
        print(str(ex))


def nedgame():
    try:
        store = ['nedgame', 'NedGame']
        req = requests.get(shops[store[0]]['urls'][prod], headers={
                           'User-Agent': get_random_ua(), 'referer': random.choice(referers)})
        print("{} - {} - {}".format(store[1], req.status_code, req.reason))
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("div", {"class": "button koopbutton"})
        if in_cart == None:
            print("Out of stock")
        elif in_cart != None:
            print("In stock!!")
            send_notification(store[1], shops[store[0]]['urls'][prod])
    except Exception as ex:
        print('Exception in Nedgam', flush=True)
        print(str(ex))


def nedgame2():
    try:
        store = ['nedgame2', 'NedGame']
        req = requests.get(shops[store[0]]['urls'][prod], headers={
                           'User-Agent': get_random_ua(), 'referer': random.choice(referers)})
        print("{} - {} - {}".format(store[1], req.status_code, req.reason))
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("div", {"class": "button koopbutton"})
        if in_cart == None:
            print("Out of stock")
        elif in_cart != None:
            print("In stock!!")
            send_notification(store[1], shops[store[0]]['urls'][prod])
    except Exception as ex:
        print('Exception in Nedgam', flush=True)
        print(str(ex))


def bol():
    try:
        store = ['bol', 'Bol.com']
        req = requests.get(shops[store[0]]['urls'][prod], headers={
                           'User-Agent': get_random_ua(), 'referer': random.choice(referers)})
        print("{} - {} - {}".format(store[1], req.status_code, req.reason))
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("div", {"class": "buy-block__options"})
        in_cart_text = in_cart.text.replace(" ", "").lower()
        if "inwinkelwagen" in in_cart_text:
            print("In stock!!")
            send_notification(store[1], shops[store[0]]['urls'][prod])
        else:
            print("Out of stock")
    except Exception as ex:
        print('Exception in Bol', flush=True)
        print(str(ex))


def gamemania():
    try:
        store = ['gamemania', 'Gamemania']
        req = requests.get(shops[store[0]]['urls'][prod], headers={
                           'User-Agent': get_random_ua(), 'referer': random.choice(referers)})
        print("{} - {} - {}".format(store[1], req.status_code, req.reason))
        soup = BeautifulSoup(req.text, 'lxml')
        in_cart = soup.find("label", {"class": "order--new"})
        in_cart_text = in_cart.text.replace(" ", "").lower()
        if not "nietbeschikbaar" in in_cart_text and 'nieuw' in in_cart_text:
            print("In stock!!")
            send_notification(store[1], shops[store[0]]['urls'][prod])
        else:
            print("Out of stock")
    except Exception as ex:
        print('Exception in Gamemania', flush=True)
        print(str(ex))


def send_notification(shop, url):
    try:
        for user in users:
            print("Message to: "+user, flush=True)
            client = Client(users[user],
                            api_token=Config.PUSHOVERTOKEN)
            client.send_message('PS5 beschikbaar bij {}. Click link:'.format(shop),
                                title="PS5 in Stock!", url=url)
    except:
        print("Error trying to send push notification")

    try:
        email = "myrdinautomail@gmail.com"
        password = Config.EMAILPW
        subject = "PS5 op voorraad bij {}".format(shop)
        message = "Link {}".format(url)

        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = ", ".join(send_to_email)
        msg["Subject"] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        server.quit()
    except:
        print("Failed to send email")


if __name__ == '__main__':
    main_loop()
