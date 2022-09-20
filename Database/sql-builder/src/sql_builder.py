import logging

from utils import *


logger = logging.getLogger(__name__)

class SqlBuilder:
    def __init__(self, input_json:dict, sql_ref:dict) -> None:
        self.input_json = None
        self.sql_ref = None
        self.tree = None
        self.input_json, self.sql_ref =\
            self.validate(input_json, sql_ref)
    
    def validate(self, input_json:dict, sql_ref:dict) -> dict:
        """
        To validate
        - input type
        - schema
        """
        if self.input_json is not None\
            or self.tree is not None\
            or self.sql_ref is not None:
            logger.warning(
                "setting input_json or tree or sql_ref to none"
            )
            self.input_json = None
            self.tree = None
            self.sql_ref = None

        if not isinstance(input_json, dict)\
            or not isinstance(sql_ref, dict):
            raise InvalidInput(
                "please input a python dictionary for input_json or sql_ref"
            )
            
        return input_json, sql_ref

    def _build(self):
        table_name = self.input_json[0]
        tmp = self.sql_ref[]

    
    def build(self) -> str:
        generated_sql_string = self._build()
        self.input_json = None
        self.tree = None
        return generated_sql_string