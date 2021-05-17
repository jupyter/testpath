Mocking system commands
=======================

.. currentmodule:: testpath

Mocking is a technique to replace parts of a system with interfaces that don't
do anything, but which your tests can check whether and how they were called.
The :mod:`unittest.mock` module in Python 3 lets you mock Python functions and
classes. The tools described here let you mock external commands.

Commands are mocked by creating a real file in a temporary directory which is
added to the :envvar:`PATH` environment variable, not by replacing Python
functions. So if you mock ``git``, and your Python code runs a shell script
which calls ``git``, it will be the mocked command that it runs.

By default, mocked commands record each call made to them, so that your test can
check these. Using the :class:`MockCommand` API, you can change what a mocked
command does.

.. note::

   Mocking a command affects all running threads or coroutines in a program.
   There's no way to mock a command for only the current thread/coroutine,
   because it uses environment variables, which are global.

.. autofunction:: assert_calls

.. autoclass:: MockCommand

   .. automethod:: fixed_output

   .. automethod:: get_calls

   .. automethod:: assert_called
