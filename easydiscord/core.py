from discord.ext import commands as _cmd
from .exceptions import *
from .utils import _no_print, _check_coro
from functools import wraps

import abc

__all__ = ["Command", "Group"]


class Command(_cmd.Command):
    """
    A subclass of python.py's :class:`Command <discord.ext.commands.Command>`.
    This should be used as the ``Command`` object.
    """
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


class Group(abc.ABC):

    def __init__(self):
        """
        This is the superclass for all grouping of commands.
        See :meth:`.add_group` for exmaples.

        Raises:
            :class:`TypeError`:
                When :meth:`register` is not overwritten by subclasses.
        """
        self.func_names = {}

    # ! make set_name support decorators
    def set_name(self, meth, name):
        """
        Sets/changes the name from the method. This function is not required, the command name
        will remain to be the method's name if :meth:`set_name()` is not called.
        After the method's name has been changed, the command will use the new name.
        Only use :meth:`set_name` in :meth:`register`.

        Args:
            meth: (:class:`method`):
                The method whom name will be changed.

            name: (:class:`str`):
                The name to change it to.

        Returns:
            The method provided by argument ``meth``.

        Examples: ::

            class Greetings(easydiscord.Group):
                @property
                def register(self):
                    self.set_name(self.hi, 'hello') # The registered command is not called 'hello'
                    return [self.hi]

                def hi(self, ctx):
                    print('hi')

            bot.add_group(Greetings)
        """

        if not hasattr(meth, '__self__'):
            self.func_names[meth.__name__] = name
        else:
            self.func_names[meth.__func__.__name__] = name
        return meth

    @property
    @abc.abstractmethod
    def register(self):
        """
        **This class must be overwritten.**

        This method should return a list of commands to register.
        If there's no command to register, this should return an empty list.

        Returns: :class:`list`:
            A list of commands to register, all commands needs to be instances.
        """
        return []


class BotBase:

    # ! add 'ignore' from severity
    def __init__(self, token, *, verbose: bool=True, severity='high'):
        """
        Args:
            token: (:class:`str`):
                Your bot's API token.

            verbose: (:class:`bool`):
                Whether or not to receive some :func:`print` messages. Defaults to :const:`True`.

            severity: (:class:`str`):
                How should none-breaking error be handled.
                If set to 'low', a warning will be raised; if set to 'high' an exception would be raised.
                Defaults to 'high'.

        Raises:
            :class:`AttributeError`:
                When severity is incorrectly set.
        """

        if not verbose:
            self.print = lambda *args, **kwargs: None
        else:
            self.print = print
        self._bot = None
        self._prefix = None
        self.token = token
        self.all_commands = {}
        if severity not in {'high', 'low'}:
            raise AttributeError("severity must be set to 'high' or 'low'")
        self.severity = severity

    @property
    def bot(self) -> _cmd.Bot:
        """
        Retrieve the background discord.py :class:`Bot <discord.ext.commands.Bot>` instance.
        Do not use this unless you have a clear idea on integrating this into your code.

        Returns:
             :class:`Bot <discord.ext.commands.Bot>`:

                A discord.py :class:`Bot <discord.ext.commands.Bot>`.

        Raises:
            :class:`.EasyDiscordError`:
                When :meth:`Bot.config()` is not called first.
        """

        if self._bot is None:
            raise EasyDiscordError(".config() or .setup() need to be called first.")
        return self._bot

    @bot.setter
    def bot(self, val):
        self._bot = val

    @property
    def prefix(self) -> str:
        """
        The prefix from your :class:`Bot`'s chat commands.

        Returns:
             :class:`str`:

                The string representation of your :class:`Bot`'s prefix.

        Raises:
            :class:`.EasyDiscordError`:
                When :meth:`Bot.config()` is not called first.
        """

        if self._prefix is None:
            raise EasyDiscordError(".config() or .setup() need to be called first.")
        return self._prefix

    @prefix.setter
    def prefix(self, val):
        self._prefix = val

    # ! help_format
    def config(self, prefix="$", default_on_ready=True, desc="", help_format=None):
        """
        Configures this :class:`Bot`.

        Args:
            prefix: (:class:`str`):
                The chat commands prefix from your :class:`Bot`. Defaults to ``'$'``.

            default_on_ready: (:class:`bool`):
                Whether nor not use the default :meth:`on_ready` message. Defaults to :const:`True`.

            desc: (:class:`str`):
                The description for the :class:`Bot`.

            help_format:
                |no-impl|

        Returns:
            :class:`Bot`:
                The :class:`Bot` itself.
        """

        self.prefix = prefix if self._prefix is None else prefix
        self.bot = _cmd.Bot(command_prefix=self.prefix, description=desc, formatter=help_format)
        if default_on_ready:
            self.add_event(self.on_ready)
        return self

    @wraps(config)
    def setup(self, *args, **kwargs):
        return self.config(*args, **kwargs)

    setup.__doc__ = "An alias of :meth:`.config()`.\n{}".format(setup.__doc__)

    def start_bot(self):
        """
        Starts the main loop of the discord bot. Do not add anything after this command.

        Returns:
            :const:`None`
        """

        self.bot.run(self.token)

    async def on_ready(self):
        """
        |coro|

        The default ``on_ready`` event. Nothing will be printed if  initial ``verbose`` is set to :const:`False`.

        The following will be printed: ::

            Logged in as:
            Bot : <bot-name>
            ID  : <bot-id>
            ------

        Returns:
             :const:`None`
        """

        self.print('Logged in as')
        self.print("Bot :", self.bot.user.name)
        self.print("ID  :", self.bot.user.id)
        self.print('------')

    async def process_message(self, message):
        """
        |coro|

        |no-impl|

        """

        await self.bot.process_commands(message)

    def reload(self):
        """
        Resets the bot. Shuts the bot down and restarts it.

        Returns:
            :const:`None`

        """

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

        async def on_message(message):
            val = await func(message)

            if val is not None:
                if not isinstance(val, str):
                    self.print("Return value of on_message is not type str. Type: {}".format(type(str)))
                    return

                await self.process_message(message)
        return on_message

    # ! more desc
    def add_event(self, func, *, name=None):
        """
        Adds an event handler. The ``name`` keyword argument can be used to override the function's name.

        Args:
            func: (:class:`function`):
                The event handler itself, it can be a coroutine or not.

            name: (:class:`str`):
                The optional replacement name for your event handler.
                If :const:`None` is passed, the function name will be used.

        Returns:
            The function provided by argument ``func``.

        Examples: ::

            def on_message(message):
                print('hi')

            bot.add_event(on_message)
        """

        if name is None:
            name = func.__name__

        func = _check_coro(func, self.severity)

        if name == 'on_message':
            func = self._on_message_wrapper(func)

        func = self.bot.listen(name)(func)
        self.print('%s has successfully been registered as an event' % name)
        return func

    # ! more info
    def add_command(self, func, *, name=None):
        """
        Adds a handler to a command. The ``name`` keyword argument can be used to override the function name.

        Args:
            func: (:class:`function`):
                The command handler itself, it can be a coroutine or not.

            name: (:class:`str`):
                The optional replacement name for your command.
                If :const:`None` is passed, the function name will be used.

        Returns:
            The function provided by argument ``func``.

        Examples: ::

            def hi(ctx):
                print('hi')

            bot.add_command(hi)
        """

        func = _check_coro(func, self.severity)

        name = func.__name__ if name is None else name
        command = _cmd.command(name=name, cls=Command)(func)
        self.all_commands[name] = command

        self.bot.add_command(command)
        self.print("Command {} is registered".format(name))
        return command

    def add_group(self, group: Group, *, name=None):
        """
        Adds a group of commands. The ``name`` keyword argument can be used to override the class name.

        Args:
            group: (:class:`Group`):
                The class of the commands.

            name: (:class:`str`):
                The optional replacement name for your group.
                If :const:`None` is passed, the class name will be used.

        Returns:
            The class provided by argument ``group``.

        Raises:
            :class:`.EasyDiscordError`:
                When the ``group`` argument isn't a subclass of :class:`Group`.

        Examples: ::

            class Greetings(easydiscord.Group):
                @property
                def register(self):
                    return [self.hi]

                def hi(self, ctx):
                    print('hi')

            bot.add_group(Greetings)
        """
        if not isinstance(group, Group):
            raise EasyDiscordError("group argument must be a subclass of easydiscord.Group.")

        group_name = type(group).__name__ if name is None else name

        for func in group.register:
            if not hasattr(func, '__self__'):
                raise AttributeError("Command to register must be an instance's method, maybe try self.{}?".format(
                    func.__name__))
            command_name = func.__self__.func_names.get(func.__func__.__name__, func.__func__.__name__)

            with _no_print(self):
                command = self.add_command(func, name=command_name)
                setattr(command, 'cog_name', group_name)

            self.print("Command {} of {} is registered".format(command.name, group_name))

        return group
