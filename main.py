from bs4 import BeautifulSoup
import requests
import time


urls = ['https://www.coolblue.nl/product/865866/playstation-5.html', 
        'https://www.coolblue.nl/product/869587/sony-playstation-5-dualsense-draadloze-controller.html']
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

while True:
    soup = BeautifulSoup(requests.get(urls[0], headers=headers).text, 'lxml')
    in_cart = soup.find("button", {"class": "js-add-to-cart-button"})
    if in_cart == None:
        print("Out of stock")
    elif in_cart != None:
        print("In stock!!")
    time.sleep(100)
