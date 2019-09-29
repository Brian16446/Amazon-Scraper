import collections

def read_file():
    catalog = collections.OrderedDict()

    with open('product-list.txt') as f:
        for line in f:
            itemData = line.split(",")
            key, value = itemData[0], itemData[1]
            catalog[key] = value
    
    return catalog

def add_product_to_file():
    with open("product-list.txt", "a") as f:
        print ("Enter the URL of the item you wish to track")
        product = raw_input().strip()
        print ("Enter your price limit for the product")
        priceLimit = raw_input()
        line = "{0}, {1}".format(product, priceLimit)
        f.write(line)

def write_new_catalog(catalog):
    with open('product-list.txt', 'w') as f:
        for product in catalog:
            # must be a way to consolidate this code?
            f.write(product)
            f.write(",")
            f.write(catalog[product])

def remove_product(index):
    catalog = read_file()
    x = catalog.items()[index][0]
    del catalog[x]
    write_new_catalog(catalog)

def change_product_price(index, newPrice):
    catalog = read_file()
    item = catalog.items()[index][0]
    catalog[item] = newPrice
    write_new_catalog(catalog)
