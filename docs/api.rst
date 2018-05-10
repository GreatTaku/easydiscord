.. currentmodule:: easydiscord

API Reference
=============

Importing
---------

The recommended way to import |name| is as followed: ::

    import easydiscord
    from easydiscord import *

This will import all the necessary items into your global scope.
Version Info
------------

.. data:: __version__

    A string representation of the current version.

    Returns:

        :class:`str`: The version info.

    Example: ::

        print(easydiscord.__version__)
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
