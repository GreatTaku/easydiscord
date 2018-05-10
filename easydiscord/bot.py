from .core import BotBase
import asyncio

__all__ = ['Bot']


class Bot(BotBase):
    """
    The ``Bot`` object that represents a discord bot.

    Call :meth:`.config()` method after that bot is initiated.
    """

    @asyncio.coroutine
    def reply(self, msg, reply_message):
        yield from self.bot.send_message(msg.channel, msg=replay_message)
