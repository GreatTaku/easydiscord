from .core import BotBase
from .exceptions import EasyDiscordError
from discord import TextChannel as _channel

__all__ = ['Bot']


class Bot(BotBase):
    """
    The ``Bot`` object that represents a discord bot.

    Call :meth:`.config()` method after that bot is initiated.
    """

    async def reply(self, current, reply_message):
        if hasattr(current, "channel"):
            channel = current.channel
        elif not isinstance(current, _channel):
            raise EasyDiscordError("Cannot reply with type {}".format(type(current)))

        await channel.send(content=reply_message)
