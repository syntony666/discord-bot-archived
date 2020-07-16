from pymongo import MongoClient

def getDatabase():
    username = 'admin'
    password = '1gDBfQklGazHlNeo'
    dbName = 'bot-db'
    db = MongoClient(f'mongodb+srv://{username}:{password}@discordbotdb-iopzr.gcp.mongodb.net/{dbName}?retryWrites=true&w=majority')
    return db[dbName]
