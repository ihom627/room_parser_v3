""" Parses the Ensemble product data """
import json
import sys
    
def parse_json_once(product, attribute):
    """ Parses a single Ensemble product's data """
    name = attribute["name"]
    
    rot = product["rot"] / 32.0 * 360.0
    pos = [ product["pos"]["x"], product["pos"]["y"], 0.0 ]
    layer = attribute["layer"]
    brand = attribute["brand"]
    
    sku = product["sku"]
    oman = product["product"]
    fabric = product["fabric"]
    
    depth = 0
    width = 0
    height = 0
    
    try:
        depth = attribute["depth"]
        width = attribute["width"]
        height = attribute["height"]
    except:
        pass
    
    return {"fabric": fabric, "oman": oman, "name": name, "pos": pos,
        "rot": rot, "layer": layer, "depth": depth, "width": width, "height": height,
        "sku": sku, "brand": brand }

def match_attribute(product, attribute_array):
    """ match the product with an attribute """
    attribute = None
    for attribute_cur in attribute_array:
        if attribute_cur["name"] == product["product"]:
            attribute = attribute_cur
            break
    return attribute

def fix_fabric(product):
    """ fix the product missing attribute """
    if 'fabric' not in product:
        product["fabric"] = "missing"
    return product

def parse_json(data):
    """ Parses the Ensemble product data """
    output = []
    try:
        if "products" in data:
            attribute_array = data["productAttributes"]
            fabric_array = data["fabricAttributes"]
            product_array = data["products"]
            if product_array["version"] == "1.0.3":
                product_array = product_array["products"]
                for i in range(len(product_array)):
                    product = product_array[i]
                    attribute = match_attribute(product, attribute_array)
                    product = fix_fabric(product)
                    if attribute != None:
                        data = parse_json_once(product, attribute)
                        output.append(data)
    except:
        print("products parse failure")
    return output

if __name__ == '__main__':
    with open("example.json") as file:
        data = json.load(file)
        output = parse_json(data)
        print(output)
