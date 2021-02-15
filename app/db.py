from tinydb import TinyDB, Query


db = TinyDB('db.json')
db.insert({123: "value"})
