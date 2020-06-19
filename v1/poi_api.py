from colorama import Fore, init

init()


def get_value(path, obj):
    toRet = []
    if len(path) == 1:

        if obj and isinstance(obj, dict) and obj.get(path[0]):
            return obj.get(path[0])

    if len(path) > 1:
        if obj and isinstance(obj, dict) and obj.get(path[0]):
            if isinstance(obj.get(path[0]), list):
                for curObj in obj.get(path[0]):
                    toRet.append(get_value(path[1:], curObj))
            else:
                toRet.append(get_value(path[1:], obj.get(path[0])))

    if len(toRet) != 0:
        return toRet
    return None


def download_file():
    print(Fore.RED + "downloading started")
    url = "https://diffuseur.datatourisme.gouv.fr/webservice/553bf24520db65ae48916676671545d4/dfdd6504-b41b-4e6e-bde8-12937636375d"
    query = None
    local_filename = url.split('/')[-1] + ".json"
    print(url)
    # NOTE the stream=True parameter below
    with requests.post(url, stream=True, json={'query': query}) as r:
        r.raise_for_status()
        with open(local_filename, 'w+b') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
            print(f.read())
    return local_filename


def parse_file(file_name):
    print(Fore.RED + "parsing started")
    with open("dfdd6504-b41b-4e6e-bde8-12937636375d.json", errors='ignore', encoding='utf-8') as file:
        items = ijson.items(file, "@graph.item")

        for item in items:
            print(Fore.BLUE + "NEW ITEM" + Fore.RESET)
            add_place_to_db(item)


def add_place_to_db(place):
    newPlace = {
        "name": None,
        "desc": None,
        "address": None,
        "postCode": None,
        "city": None,
        "pos": None,
        "website": None,
        "phone": None,
        "mail": None,
        "image": None,
        "price": None,
    }
    print(Fore.LIGHTBLUE_EX + place.get("@id") + Fore.RESET)

    # get name
    name = get_value(["rdfs:label", "@value"], place)
    if name and len(name) > 0:
        newPlace["name"] = name[0]

    # get description
    desc = get_value(["rdfs:comment", "@value"], place)
    if desc and len(desc) > 0:
        newPlace["desc"] = desc[0]

    # get address
    address = get_value(["isLocatedAt", "schema:address", "schema:streetAddress"], place)
    if address and len(address) > 0:
        newPlace["address"] = address[0]

    # get post code
    postCode = get_value(["isLocatedAt", "schema:address", "schema:postalCode"], place)
    if postCode and len(postCode) > 0:
        newPlace["postCode"] = postCode[0]

    # get city
    city = get_value(["isLocatedAt", "schema:address", "schema:addressLocality"], place)
    if city and len(city) > 0:
        newPlace["city"] = city[0]

    # get position
    pos = get_value(["isLocatedAt", "schema:geo", "latlon", "@value"], place)
    if pos and len(pos) > 0:
        newPlace["pos"] = pos[0]

    # get website
    website = get_value(["hasContact", "foaf:homepage"], place)
    if website and len(website) > 0:
        newPlace["website"] = website[0]

    # get phone
    phone = get_value(["hasContact", "schema:telephone"], place)
    if phone and len(phone) > 0:
        newPlace["phone"] = phone[0]

    # get mail
    mail = get_value(["hasContact", "schema:email"], place)
    if mail and len(mail) > 0:
        newPlace["mail"] = mail[0]

    # get image
    image = get_value(["hasMainRepresentation", "ebucore:hasRelatedResource", "ebucore:locator", "@value"], place)
    if image and len(image) > 0:
        newPlace["image"] = image[0]

    # price
    price = [get_value(["schema:offers", "schema:priceSpecification", "schema:maxPrice"], place),
             get_value(["schema:offers", "schema:priceSpecification", "schema:minPrice"], place),
             get_value(["schema:offers", "schema:priceSpecification", "schema:price"], place)]
    if price and len(price) > 0:
        newPlace["price"] = price[0]

    print(newPlace)
    # TODO: add newPlace to db


