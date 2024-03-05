import argparse
from bson.objectid import ObjectId

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = f"mongodb://localhost:27017/"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client.mds

parser = argparse.ArgumentParser(description="Application cats")
parser.add_argument("--action", help="create, update, read, delete, delete_by_name, update_age_by_name,\
add_features, read_by_name, delete_all")
parser.add_argument("--id", help="id")
parser.add_argument("--name", help="name")
parser.add_argument("--age", help="age")
parser.add_argument("--features", help="features", nargs="+")

args = vars(parser.parse_args())
action = args["action"]
pk = args["id"]
name = args["name"]
age = args["age"]
features = args["features"]


#Реалізуйте функцію для виведення всіх записів із колекції.
def read():
    return db.cats.find()


def create(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    return db.cats.insert_one(cat)


def update(pk, name, age, features):
    new_cat = {
        "name": name,
        "age": age,
        "features": features
    }
    return db.cats.update_one({"_id": ObjectId(pk)}, {"$set": new_cat})


def delete(pk):
    return db.cats.delete_one({"_id": ObjectId(pk)})

#Реалізуйте функцію для видалення запису з колекції за ім'ям тварини.
def delete_by_name(name):
    return db.cats.delete_one({"name": name})


#Реалізуйте функцію для видалення всіх записів із колекції.
def delete_all():
    return db.cats.delete_many({})

#Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
def add_features(name, features):
    new_cat = {
        "features": {"$each": features}
    }
    return db.cats.update_one({"name": name}, {"$push": new_cat})

#Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.
def update_age_by_name(name, age):
    update_result = db.cats.update_one(
        {"name": name},
        {"$set": {"age": age}}
    )
    return update_result


#Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
def read_by_name(name):
    document = db.cats.find_one({"name": name})
    if document is not None:
        print(document)
    else:
        print("Not found")


if __name__ == "__main__":
    match action:
        case "read":
            results = read()
            [print(cat) for cat in results]
        case "create":
            result = create(name, age, features)
            print(result)
        case "update_age_by_name":
            result = update_age_by_name(name, age)
            print(result)
        case "add_features":
            result = add_features(name, features)
            print(result)
        case "update":
            result = update(pk, name, age, features)
            print(result)
        case "delete":
            result = delete(pk)
            print(result)
        case "delete_all":
            result = delete_all()
            print(result)
        case "delete_by_name":
            result = delete_by_name(name)
            print(result)
        case "read_by_name":
            read_by_name(name)
        case _:
            print("Unknown action")
