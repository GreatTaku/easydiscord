import warnings
import inspect

__all__ = ["EasyDiscordError", "EasyDiscordWarning"]


# ! add more exceptions
class EasyDiscordError(Exception):
    """
    This is an overall exception that all easydiscord functions raises when encountered a problem.
    More :class:`Exception` will be added in the future.
    """
    @classmethod
    def no_coro(cls):
        raise cls("func argument should be a coroutine, consider defining your function by using "
                  "`async def <name>(<args>):` instead of `def <name>(<args>):`. "
                  "Don't forget to `await` asynchronous functions/")


class EasyDiscordWarning(UserWarning):
    """
        This is an overall warning that all easydiscord functions raises when encountered a minor problem.
        More :class:`UserWarning` will be added in the future.
        """
    @classmethod
    def no_coro(cls):
        warnings.warn("func argument should be a coroutine, consider defining your function by using "
                      "`async def <name>(<args>):` instead of `def <name>(<args>):`. "
                      "Don't forget to `await` asynchronous functions/", cls, len(inspect.stack()))
