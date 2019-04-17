from pymongo import MongoClient

def connectiondb():
    client = MongoClient('127.0.0.1', 27017)
    db = client['pent']
    dbcollection = db['subdomain']
    return dbcollection