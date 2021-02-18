from tinydb import Query, TinyDB


class TDB:
    def __init__(self, db: TinyDB):
        self.db = db

    def add_or_update_value(self, key: str, value):
        if self.get_value(key):
            self.db.update({"value": value}, Query().key == key)
        else:
            self.db.insert({"key": key, "value": value})

    def get_value(self, key: str) -> str:
        values = self.db.search(Query().key == key)

        try:
            return values[0]["value"]
        except IndexError:
            return ""


db = TinyDB("db.json")
db = TDB(db)
