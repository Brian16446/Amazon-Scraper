import files as f
import requests
from bs4 import BeautifulSoup
import smtplib

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}

def view_catalog():
    catalog = f.read_file()
    i = 1
    for item in  catalog:
        title = get_product_title(item)
        print "{0}) {1}".format(i, title)
        i += 1


def check_price(product, priceLimit):
    
    page = requests.get(product, headers=headers)

    soup = BeautifulSoup(page.content, "lxml")
    text_price = soup.find("span", {"class": "offer-price"}).get_text()
    price = float(text_price[1:]) # Removing the £ symbol and converting to float

    title = soup.find(id="productTitle").get_text()

    print(title.strip())
    print(price)

    if(price < priceLimit):
        send_mail(product);
    
def check_all_prices():
    catalog = f.read_file()
    for item in catalog:
        # removing the \n character from value and converting to float
        price = float(catalog[item].strip())
        check_price(item, price) # passing the itemURL and the price


def get_product_title(product):
    page = requests.get(product, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    title = soup.find(id="productTitle").get_text()
    return title

def send_mail(product):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('brianbridge2012@gmail.com', 'hagtvtifrbpjuwww')

    subject = 'A product you have watched has fell down!'
    body = 'Here is a link to the product: {0}'.format(product)

    msg = "Subject: {0}\n\n{1}".format(subject, body)

    server.sendmail(
        'brianbridge2012@gmail.com',
        'brianbridge@live.co.uk',
        msg
    )

    print("Email sent")
    server.quit()

print "======= Amazon Product Watch ======="
print "= 1: Check prices                  ="
print "= 2: View catalog                  ="
print "= 3: Add new product               ="
print "= 4: Remove a product              ="
print "= 5: Change a products price limit ="
print "= 6: Exit                          ="
print "===================================="

choice = input()

if(choice == 1):
    check_all_prices()
elif (choice == 2):
    print "Loading products..."
    view_catalog()
elif(choice == 3):
    f.add_product_to_file()
elif(choice == 4):
    print ("Loading products...")
    view_catalog()
    print ("Choose a product to delete: ")
    choice = input()
    # need to get length of array and validate the choice
    choice -= 1 # adjusting for zero index of dict
    f.remove_product(choice) # could add return true or false to this to confirm if done
    print ("product removed")
elif(choice == 5):
    print ("Loading products...")
    view_catalog()
    print ("Choose a price to ammend: ")
    choice = input()
    # add error control
    choice -= 1
    print ("Enter new price: ")
    newPrice = raw_input() # needs to be a string
    # add error control
    f.change_product_price(choice, newPrice)
    print ("Price amended")
else:
    print ("Please select a valid option: 1-5")