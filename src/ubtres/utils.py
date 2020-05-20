from ubtres import db
from ubtres.models import Result
import json

def get_defconfig_data(defconfig, count):
    result = Result.query.filter(Result.defconfig==defconfig).all()
    if result == None:
        return None, None

    i = 0
    ids = []
    dates = []
    images = []
    for res in reversed(result):
        d = res.to_dict()
        ids.insert(0, res.id)
        dates.insert(0, d["basecommit"])
        images.insert(0, d["images"])
        i += 1
        if i == count:
            return ids, dates, images

    return ids, dates, images

def get_images_names(images):
    names = []
    for img in images:
        js_string = json.loads(img)
        for n in js_string:
            if n["name"] not in names:
                names.append(n["name"])

    return names

def get_images_value(img, name):
    """
    search in img if name is found
    if so, return value
    else -1
    """
    js_string = json.loads(img)
    for n in js_string:
        if n["name"] == name:
            return int(n["size"])
    return -1

def convert_images_to_picture(images):
    names = get_images_names(images)
    pic = []
    # search for all names
    for n in names:
        values = []
        for img in images:
            values.append(get_images_value(img, n))
        pic.append({"name":n, "values":values})

    return pic
