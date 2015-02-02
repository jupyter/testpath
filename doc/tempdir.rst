Utilities for temporary directories
===================================

.. module:: testpath.tempdir

This module exposes :func:`tempfile.TemporaryDirectory`, with a backported copy
so that it can be used on Python 2. In addition, it contains:

.. autoclass:: NamedFileInTemporaryDirectory

.. autoclass:: TemporaryWorkingDirectory
