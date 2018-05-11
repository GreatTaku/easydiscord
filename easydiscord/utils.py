from contextlib import contextmanager
import asyncio

from .exceptions import *


@contextmanager
def _no_print(self):
    _print = self.print
    self.print = lambda *args, **kwargs: None
    yield
    self.print = _print


def _check_coro(func, severity):
    if not asyncio.iscoroutinefunction(func):
        if severity == 'low':
            EasyDiscordWarning.no_coro()
            func = asyncio.coroutine(func)
        elif severity == 'high':
            EasyDiscordError.no_coro()
        else:
            raise NotImplementedError
    return func
