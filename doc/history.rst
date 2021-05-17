Release notes
=============

0.5
---

* Easier ways to use :class:`.MockCommand` to customise mocked commands,
  including ``python=`` to specify extra code to run,
  :meth:`~.MockCommand.fixed_output`, and :meth:`~.MockCommand.assert_called`.
* Command mocking will use :data:`os.defpath` as the initial PATH if the PATH
  environment variable is not set.

May 2021