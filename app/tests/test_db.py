import os
from unittest import TestCase

from tinydb import Query, TinyDB

from app.db import TDB


class DBTestCase(TestCase):
    db_path = "test_db.json"
    first_value = {"key": "111", "value": "test value 1"}

    def setUp(self):
        self.db = TinyDB(self.db_path)
        self.db_wrapper = TDB(self.db)
        self.db.insert(self.first_value)

    def tearDown(self):
        self.db.close()
        os.unlink(self.db_path)

    def test_init_db(self):
        self.assertEqual(len(self.db.all()), 1)

    def test_add_value(self):
        test_key = "222"
        test_value = "test value 2"

        self.db_wrapper.add_or_update_value(test_key, test_value)
        Value = Query()
        values = self.db.search(Value.key == test_key)
        self.assertEqual(values[0]["value"], test_value)

    def test_update_value(self):
        test_key = "222"
        test_value = "test value 2 edited"

        self.db_wrapper.add_or_update_value(test_key, test_value)
        Value = Query()
        values = self.db.search(Value.key == test_key)
        self.assertEqual(values[0]["value"], test_value)

    def test_get_existing_value(self):
        value = self.db_wrapper.get_value(self.first_value["key"])

        self.assertEqual(value, self.first_value["value"])

    def test_get_non_existing_value(self):
        non_exinting_key = "444"

        value = self.db_wrapper.get_value(non_exinting_key)

        self.assertEqual(value, "")
