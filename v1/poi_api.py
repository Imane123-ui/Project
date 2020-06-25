from colorama import Fore, init
import ijson
import requests
from . import models

init()


# getting all value matching the "path" in the "obj" object
def get_value(path, obj):
    toRet = []
    if len(path) == 1:
        if obj and isinstance(obj, dict) and obj.get(path[0]):
            return obj.get(path[0])

    if len(path) > 1:
        if obj and isinstance(obj, dict) and obj.get(path[0]):
            if isinstance(obj.get(path[0]), list):
                for curObj in obj.get(path[0]):
                    res = get_value(path[1:], curObj)
                    if isinstance(res, list):
                        toRet.extend(res)
                    else:
                        toRet.append(res)
            elif obj.get(path[0]):
                res = get_value(path[1:], obj.get(path[0]))
                if isinstance(res, list):
                    toRet.extend(res)
                else:
                    toRet.append(res)

    if len(toRet) != 0:
        toRet = [i for i in toRet if i]
        return toRet
    return None


# download file with all POI from the API
def download_file():
    print(Fore.RED + "downloading started")
    url = "https://diffuseur.datatourisme.gouv.fr/webservice/553bf24520db65ae48916676671545d4/dfdd6504-b41b-4e6e-bde8-12937636375d"
    query = None
    local_filename = url.split('/')[-1] + ".json"
    # NOTE the stream=True parameter below
    with requests.post(url, stream=True, json={'query': query}) as r:
        r.raise_for_status()
        with open(local_filename, 'w+b') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return local_filename


# go through the downloaded file and add needed data to db
def parse_file(file_name):
    with open("dfdd6504-b41b-4e6e-bde8-12937636375d.json", errors='ignore', encoding='utf-8') as file:
        items = ijson.items(file, "@graph.item")

        for item in items:
            add_place_to_db(item)


# adding needed place's data to db
def add_place_to_db(place, weathers):
    newPlace = {
        "name": None,
        "desc": None,
        "address": None,
        "postCode": None,
        "city": None,
        "lat": None,
        "long": None,
        "website": None,
        "phone": None,
        "mail": None,
        "image": None,
        "price": None,
    }
    b = models.Place()

    # get name
    name = get_value(["rdfs:label", "@value"], place)
    if name and len(name) > 0:
        newPlace["name"] = name[0]
        b.Name_Place = newPlace["name"]

    # get description
    desc = get_value(["rdfs:comment", "@value"], place)
    if desc and len(desc) > 0:
        newPlace["desc"] = desc[0]
        b.Description_Place = newPlace["desc"]

    # get address
    address = get_value(["isLocatedAt", "schema:address", "schema:streetAddress"], place)
    if address and len(address) > 0:
        newPlace["address"] = address[0]
        b.Address_Place = newPlace["address"]

    # get post code
    postCode = get_value(["isLocatedAt", "schema:address", "schema:postalCode"], place)
    if postCode and len(postCode) > 0:
        newPlace["postCode"] = postCode[0]

    # get city
    city = get_value(["isLocatedAt", "schema:address", "schema:addressLocality"], place)
    if city and len(city) > 0:
        newPlace["city"] = city[0]
        b.City_Place = newPlace["city"]

    # get position
    pos = get_value(["isLocatedAt", "schema:geo", "latlon", "@value"], place)
    if pos and len(pos) > 0:
        pos_split = pos[0].split("#")
        newPlace["lat"] = pos_split[0]
        newPlace["long"] = pos_split[1]
        b.Latitude_Place = newPlace["lat"]
        b.Longitude_Place = newPlace["long"]
        distances = []
        for weather in weathers:
            distances.append(distance2points(weather.Latitude_Weather, weather.Longitude_Weather, newPlace["lat"],
                                             newPlace["long"]))
        minDist = getMinDist(distances)
        curWeathers = models.Weather.objects.all().filter(Latitude_Weather=minDist[1], Longitude_Weather=minDist[2])[:5]
        b.save()
        for curWeather in curWeathers:
            b.Weather_Place.add(curWeather)

    # get website
    website = get_value(["hasContact", "foaf:homepage"], place)
    if website and len(website) > 0:
        newPlace["website"] = website[0]

    # get phone
    phone = get_value(["hasContact", "schema:telephone"], place)
    if phone and len(phone) > 0:
        newPlace["phone"] = phone[0]
        b.Phone_Place = newPlace["phone"]

    # get mail
    mail = get_value(["hasContact", "schema:email"], place)
    if mail and len(mail) > 0:
        newPlace["mail"] = mail[0]

    # get image
    image = get_value(["hasMainRepresentation", "ebucore:hasRelatedResource", "ebucore:locator", "@value"], place)
    if image and len(image) > 0:
        newPlace["image"] = image[0]
        b.Photo_Place = newPlace["image"]

    # price
    price = []
    maxPrice = get_value(["schema:offers", "schema:priceSpecification", "schema:maxPrice", "@value"], place)
    minPrice = get_value(["schema:offers", "schema:priceSpecification", "schema:minPrice", "@value"], place)
    defPrice = get_value(["schema:offers", "schema:priceSpecification", "schema:price", "@value"], place)
    if maxPrice:
        price.extend(maxPrice)
    if defPrice:
        price.extend(defPrice)
    if minPrice:
        price.extend(minPrice)
    if price and len(price) > 0:
        newPlace["price"] = price[0]
        b.Price_Place = newPlace["price"]

    # TODO: add newPlace to db

    b.save()
