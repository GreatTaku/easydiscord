try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install

import sys

if sys.version_info[0:2] < (3, 4):
    raise Exception("Python 3.4+ is required.")
else:
    from pathlib import Path

__version__ = "0"
with open(Path("./easydiscord/__init__.py"), 'r') as f:
    from re import search
    _version = search(r"__version__\s*=\s*\'(.*?)\'", f.read())
    if _version is not None:
        __version__ = _version.group(1)


try:
    with open(Path("./README.rst"), 'r') as f:
        README = f.read()
except FileNotFoundError:
    README = ''


class PostInstallCommand(install):

    def run(self):
        super().run()
        try:
            from pip import main
        except ImportError:
            from pip._internal import main

        main(['install', 'https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py[voice]'])


setup(name='easydiscord',
      author='Taku',
      url='None Yet',
      version=__version__,
      packages=['easydiscord'],
      license='MIT',
      description='An easy to use wrapper for Discord.py',
      long_description=README,
      include_package_data=True,
      cmdclass={'install': PostInstallCommand},
      python_requires='>=3.4',
      keywords='discord.py easy simple discord python',
      classifiers=[
          'Development Status :: 1 - Planning',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
      ]
      )
