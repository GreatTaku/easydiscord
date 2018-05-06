__version__ = '0.1a0.dev0'

from .core import *
from .bot import *


def get_bot(token):
    return Bot(token)
