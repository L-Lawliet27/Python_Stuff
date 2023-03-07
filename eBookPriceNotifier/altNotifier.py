import json
import os
import smtplib
import time
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def waitForLoad(driver):
    # Scroll to the bottom of the page and wait for new items to load
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # wait for new items to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def correctLink(link, domain):
    return f"{domain}{link[4:14]}"

def getBooks(url,domain):
    books = {}
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    waitForLoad(driver)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    bookList = soup.find('ul', {
                         "id": "g-items", "class": "a-unordered-list a-nostyle a-vertical a-spacing-none g-items-section ui-sortable"})

    for li in bookList.find_all('li', {"class": "a-spacing-none g-item-sortable", "data-id": "2QET0OTQYRWDI"}):
        title = li.find('h2', {"class": "a-size-base"})
        priceTag = li.find('span', {"class": "a-price"})
        link = title.find('a').get('href')
        parsedLink = correctLink(link,domain)
        name = title.find('a').text.strip()
        if ':' in name:
            name = name.split(':')[0].rstrip()
        elif ' (' in name:
            name = name.split(' (')[0].rstrip()
        price_tag = priceTag.find('span', {"class": "a-offscreen"})
        price = float(price_tag.text.split('€')[0].rstrip().replace(',', '.'))
        books[name] = {"price": price, "link": parsedLink}
    return books


def save(wishlist):
    with open('booksInfo.json', 'w') as file:
        json.dump(wishlist, file)


def lookForChange(previous, onWishlist):
    toSend = {}
    if previous != onWishlist:
        for name in previous:
            if name in onWishlist:
                if onWishlist[name]["price"] < previous[name]["price"]:
                    toSend[name] = {"price": onWishlist[name]
                                    ["price"], "link": onWishlist[name]["link"]}
        save(onWishlist)
    return toSend


def getDataToString(toSend):
    message = '\n'.join(
        [f"{name} - {toSend[name]['price']} \n{toSend[name]['link']}\n" for name in toSend])
    return message


def sendMail(toSend, userEmail, appPasswd):
    msg = MIMEText(getDataToString(toSend))
    msg['Subject'] = 'Price-Drop Notification'
    msg['From'] = userEmail
    msg['To'] = userEmail

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(userEmail, appPasswd)
        smtp.sendmail(userEmail, userEmail, msg.as_string())
        smtp.quit()


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    userInfo = json.load(open('info.json'))
    url = userInfo.get("wishlist")
    domain = userInfo.get("domain")
    userEmail = userInfo.get("my_email")
    appPasswd = userInfo.get("sender_pswd")
    onWishlist = getBooks(url,domain)
    previous = json.load(open('booksInfo.json'))
    toSend = lookForChange(previous, onWishlist)
    if toSend:
        sendMail(toSend, userEmail, appPasswd)


if __name__ == '__main__':
    main()
