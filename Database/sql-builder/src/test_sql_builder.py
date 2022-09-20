import unittest

from sql_builder import SqlBuilder
from utils import *

class TestSqlBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.sb = SqlBuilder

    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_sql_builder_validate(self):
        with self.assertRaises(InvalidInput):
            self.sb(["1"], "2")

        self.sb({}, {})
    
    def test_select_simple(self):
        pass

    def test_select_complex(self):
        pass

    def test_select_join(self):
        pass