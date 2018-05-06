import asyncio

from discord.ext import commands as _cmd
from .exceptions import EasyDiscordError
from .utils import _no_print

__all__ = ["Command", "Group", "BotBase"]


class Command(_cmd.Command):

    def __init__(self, name, callback, **kwargs):
        super().__init__(name, callback, **kwargs)
        self._cog_name = None

    @property
    def cog_name(self):
        if self._cog_name is not None:
            return self._cog_name
        elif self.instance is not None:
            return type(self.instance).__name__
        return None

    @cog_name.setter
    def cog_name(self, val):
        self._cog_name = val


class Group:

    def __init__(self):
        self.func_names = {}

    def set_name(self, func, name):
        self.func_names[func.__func__.__name__] = name
        return func

    @property
    def register(self):
        return []


class BotBase:
    def __init__(self, token, *, no_print=False):
        if no_print:
            self.print = lambda *args, **kwargs: None
        else:
            self.print = print
        self._bot = None
        self._prefix = None
        self.token = token
        self.all_commands = {}

    @property
    def bot(self) -> _cmd.Bot:
        if self._bot is None:
            raise EasyDiscordError(".config() need to be called first.")
        return self._bot

    @bot.setter
    def bot(self, val):
        self._bot = val

    @property
    def prefix(self) -> str:
        if self._prefix is None:
            raise EasyDiscordError(".config() need to be called first.")
        return self._prefix

    @prefix.setter
    def prefix(self, val):
        self._prefix = val

    def config(self, prefix="$", default_on_ready=True, desc="", help_format=None):
        self.prefix = prefix
        self.bot = _cmd.Bot(command_prefix=self.prefix, description=desc, formatter=help_format)
        if default_on_ready:
            self.add_event(self.on_ready)

    def start_bot(self):
        self.bot.run(self.token)

    @asyncio.coroutine
    def on_ready(self):
        self.print('Logged in as')
        self.print("Bot:", self.bot.user.name)
        self.print("ID:", self.bot.user.id)
        self.print('------')

    @asyncio.coroutine
    def process_message(self, message):
        yield from self.bot.process_commands(message)

    def reload(self):
        self.bot.clear()

    def __getattr__(self, attr):
        if attr in {'loop', 'user', 'guilds', 'emojis', 'private_channels', 'voice_clients',
                    'is_ready', 'is_closed', 'dispatch', 'on_error', 'activity', 'get_channel',
                    'get_guild', 'get_user', 'get_emoji', 'get_all_channels', 'get_all_members',
                    'change_presence', 'get_user_info', 'close'}:
            self.print("{} might not work correctly, as it had not been implemented yet.".format(attr))
            return getattr(self.bot, attr)
        else:
            return self.__getattribute__(attr)

    def _on_message_wrapper(self, func):
        @asyncio.coroutine
        def on_message(message):
            val = yield from func(message)
            if val:
                yield from self.process_message(message)

        return on_message

    def add_event(self, func, event_name=None):

        if event_name is None:
            event_name = func.__name__

        if not asyncio.iscoroutinefunction(func):
            func = asyncio.coroutine(func)

        if event_name == 'on_message':
            func = self._on_message_wrapper(func)

        func = self.bot.listen(event_name)(func)
        self.print('%s has successfully been registered as an event' % event_name)
        return func

    def add_command(self, func, *, name=None):
        if not asyncio.iscoroutinefunction(func):
            func = asyncio.coroutine(func)

        name = func.__name__ if name is None else name
        command = _cmd.command(name=name, cls=Command)(func)
        self.all_commands[name] = command

        self.bot.add_command(command)
        self.print("Command {} is registered".format(name))
        return command

    def add_group(self, group, *, name=None):
        group_name = type(group).__name__ if name is None else name

        for func in group.register:
            if not hasattr(func, '__self__'):
                raise AttributeError("Registered command must be an instances method, maybe try {}?".format(
                    func.__name__))
            command_name = func.__self__.func_names.get(func.__func__.__name__, func.__func__.__name__)

            with _no_print(self):
                command = self.add_command(func, name=command_name)
                setattr(command, 'cog_name', group_name)

            self.print("Command {} of {} is registered".format(command.name, group_name))
