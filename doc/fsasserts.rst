Assertion functions for the filesystem
======================================

These functions make it easy to check the state of files and directories.
When the assertion is not true, they provide informative error messages.

.. module:: testpath

.. autofunction:: assert_path_exists

.. autofunction:: assert_not_path_exists

.. autofunction:: assert_isfile

.. autofunction:: assert_not_isfile

.. autofunction:: assert_isdir

.. autofunction:: assert_not_isdir

.. autofunction:: assert_islink

.. autofunction:: assert_not_islink

Unix specific
-------------

.. versionadded:: 0.4

These additional functions test for special Unix filesystem objects: named pipes
and Unix domain sockets. The functions can be used on all platforms, but these
types of objects do not exist on Windows.

.. autofunction:: assert_ispipe

.. autofunction:: assert_not_ispipe

.. autofunction:: assert_issocket

.. autofunction:: assert_not_issocket
