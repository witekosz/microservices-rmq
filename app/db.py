from tinydb import Query, TinyDB


db = TinyDB("db.json")
db.insert({123: "value"})
