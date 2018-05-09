.. currentmodule:: easydiscord

API Reference
=============

Importing
---------

The recommended way to import |name| is as followed: ::

    import easydiscord as discord

In the following documentation, |name| will be referenced as ``discord``.

Version Info
------------

.. data:: __version__

    A string representation of the current version.

    Returns:

        :class:`str`: The version info.

    Example: ::

        print(discord.__version__)
        "0.1a0.dev0"

Initiative Functions
--------------------

.. autofunction:: get_bot

The Bot Class
-------------

.. autoclass:: Bot
    :members:
    :undoc-members:
    :inherited-members:

Other Objects
-------------

.. autoclass:: Command

.. autoclass:: Group
    :members:
    :undoc-members:

Exceptions
----------

.. automodule:: easydiscord.exceptions
    :members:
    :undoc-members:
