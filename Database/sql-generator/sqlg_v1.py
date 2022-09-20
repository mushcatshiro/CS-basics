import logging
from .utils import IncorrectFormatter

logger = logging.getLogger(__name__)


class SQLGeneratorV1:
    def __init__(self, sql_string: str, sql_helper: dict, config: dict):
        self.sql_string = sql_string  # base SQL string from sql_utils with undefined replacement variables
        self.sql_helper = sql_helper  # replacement variables

    def _validate_replace_dict(self, replace_dict):  # replace_dict is payload dictionary with replacement variables and sql_helpers defined
        if sorted(self.sql_helper.keys()) != sorted(replace_dict.keys()):
            raise IncorrectFormatter('unable to replace dict in formatting sql string')

    def format_sql_string(self, replace_dict: dict):  # better than using placeholders (v1,v2) as order from payload doesn't matter 
        if replace_dict == {}:
            return self
        self._validate_replace_dict(replace_dict)
        for k, v in replace_dict.items():
            target = '{' + k + '}'  # {some_id}
            if isinstance(v, list):
                replacement_string = self.sql_helper[k]['list']
                v = ", ".join(['\'' + i + '\'' for i in v])
                replacement_string = replacement_string.replace(target, v)
                self.sql_string = self.sql_string.replace(target, replacement_string)
            elif v == 'placeholder':
                # omitting query field i.e. request_id = request_id
                # to be optimized due to security concerns
                replacement_string = self.sql_helper[k]['str']
                replacement_string = replacement_string.replace(target, k)
                self.sql_string = self.sql_string.replace(target, replacement_string)
            elif 'OID' in self.sql_helper[k].keys():
                replacement_string = self.sql_helper[k]['OID']
                replacement_string = replacement_string.replace(target, v)
                self.sql_string = self.sql_string.replace(target, replacement_string)
            elif isinstance(v, str):
                replacement_string = self.sql_helper[k]['str']  # some_id = {some_id}
                if 'LIKE' in replacement_string:
                    v = '\'%' + v + '%\''
                else:
                    v = '\'' + v + '\''
                replacement_string = replacement_string.replace(target, v)  # some_id = '\ 1234567.000 \'
                self.sql_string = self.sql_string.replace(target, replacement_string)
            elif isinstance(v, int):
                replacement_string = self.sql_helper[k]['int']
                replacement_string = replacement_string.replace(target,str(v))
                self.sql_string = self.sql_string.replace(target, replacement_string)
            elif v is None:
                self.sql_string = self.sql_string.replace(target, '')
        logger.debug(self.sql_string)
        return self