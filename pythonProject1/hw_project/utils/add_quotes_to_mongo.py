import json
from bson.objectid import ObjectId

from pymongo import MongoClient

client = MongoClient("mongodb+srv://Andriiok:8748@atlascluster.ghgmoal.mongodb.net/hw?retryWrites=true&w=majority")

db = client.hw

with open('quotes.json', 'r', encoding='utf=8') as fd:
    quotes = json.load(fd)

for quote in quotes:
    author = db.authors.find_one({'fullname': quote['author']})
    if author:
        db.quotes.insert_one({
            'quote': quote['quote'],
            'keywords': quote['keywords'],
            'author': ObjectId(author['_id'])
        })