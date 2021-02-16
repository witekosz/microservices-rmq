import os
from unittest import TestCase

from tinydb import TinyDB, Query

from app import db as db_module


class DBTestCase(TestCase):
    db_path = "test_db.json"
    first_value = {"key": "111", "value": "test value 1"}

    def setUp(self):
        self.db = TinyDB(self.db_path)
        self.db.insert(self.first_value)

    def tearDown(self):
        self.db.close()
        os.unlink(self.db_path)

    def test_init_db(self):
        self.assertEqual(len(self.db.all()), 1)

    def test_add_value(self):
        test_key = "222"
        test_value = "test value 2"

        db_module.db_add_or_update_value(test_key, test_value, db=self.db)
        Value = Query()
        values = self.db.search(Value.key == test_key)
        self.assertEqual(values[0]["value"], test_value)

    def test_update_value(self):
        test_key = "222"
        test_value = "test value 2 edited"

        db_module.db_add_or_update_value(test_key, test_value, db=self.db)
        Value = Query()
        values = self.db.search(Value.key == test_key)
        self.assertEqual(values[0]["value"], test_value)

    def test_get_existing_value(self):
        value = db_module.db_get_value(self.first_value["key"], db=self.db)

        self.assertEqual(value, self.first_value["value"])

    def test_get_non_existing_value(self):
        non_exinting_key = "444"

        value = db_module.db_get_value(non_exinting_key, db=self.db)

        self.assertEqual(value, None)
