__version__ = '0.1a0'

from .core import *
from .bot import *


# ! Add doc for api token link to how to obtain a token
def get_bot(token: str, *args, **kwargs):
    """
    Generates a new :class:`Bot` instance.
    You should avoid calling :class:`Bot()` directly,
    instead, use this :func:`get_bot()` constructor.

    Args:

        token: (:py:class:`str`): Your bot's API token.

    Keyword Args:

        verbose: (:py:class:`bool`): Whether or not certain messages should be printed using :py:func:`print()`.
                                     Defaults to :py:const:`True`.

    Returns:

        An instance of :class:`Bot`.

    Examples: ::

        bot = discord.get_bot("MY_API_TOKEN")

    """
    return Bot(token, *args, **kwargs)

