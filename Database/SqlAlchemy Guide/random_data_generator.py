from enum import Enum
from math import floor
import random
import string
from typing import List


class RDG:
    """
    random text generator for database testing

    backlog
    - [] how to work with Enum(s)?
    """

    def __init__(self,
                 args: List[str] = None,
                 tlen: int = 8,
                 mint: int = 10,
                 enum: Enum = None):
        self.args = args
        self.letters = string.ascii_letters
        self.tlen = tlen  # text length, avoiding collision with len
        self.mint = mint  # max int

    def __call__(self):
        ret = {}
        for arg in self.args:
            if arg.endswith('_int'):
                ret[arg] = self.ranInt(self.mint)
            elif arg.endswith('_bool'):
                ret[arg] = self.ranBool()
            else:
                ret[arg] = self.ranText(self.tlen)
        return ret

    def ranText(self, tlen):
        return ''.join(random.choice(self.letters) for i in range(tlen))

    def ranInt(self, mint):
        return floor(random.random() * mint)

    def ranBool(self):
        return random.choice([True, False])

    def ranEnum(self, ienum):
        return random.choice(ienum)
