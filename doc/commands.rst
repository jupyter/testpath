Mocking system commands
=======================

Mocking is a technique to replace parts of a system with interfaces that don't
do anything, but which your tests can check whether and how they were called.
The :mod:`unittest.mock` module in Python 3 lets you mock Python functions and
classes. These tools let you mock external commands.

Commands are mocked by creating a real file in a temporary directory which is
added to the :envvar:`PATH` environment variable, not by replacing Python
functions. So if you mock ``foo``, and your Python code runs a shell script
which calls ``foo``, it will be the mocked command that it runs.

By default, mocked commands record each call made to them, so that your test can
check these. Using the :class:`MockCommand` API, you can mock a command to do
something else.

.. note::

   These tools work by changing global state. They're not safe to use if
   commands may be called from multiple threads or coroutines.

.. currentmodule:: testpath

.. autofunction:: assert_calls

.. autoclass:: MockCommand
   :members: get_calls
