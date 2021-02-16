from tinydb import Query, TinyDB


db = TinyDB("db.json")


def db_add_or_update_value(key: str, value, db=db):
    db.insert({"key": key, "value": value})


def db_get_value(key: str, db=db) -> str:
    Value = Query()
    values = db.search(Value.key == key)

    try:
        return values[0]["value"]
    except IndexError:
        return None
