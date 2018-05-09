
__all__ = ["EasyDiscordError"]


# ! add more exceptions
class EasyDiscordError(Exception):
    """
    This is an overall exception that all easydiscord functions raises when encountered a problem.
    More :class:`Exception`s will be added in the future.
    """
    pass
