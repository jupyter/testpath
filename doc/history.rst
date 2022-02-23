Release notes
=============

0.6
---

February 2022

* Removed some code that's unused since dropping Python 2 support.
* Relax the version constraint for the ``flit_core`` build requirement.

0.5
---

May 2021

* Easier ways to use :class:`.MockCommand` to customise mocked commands,
  including ``python=`` to specify extra code to run,
  :meth:`~.MockCommand.fixed_output`, and :meth:`~.MockCommand.assert_called`.
* Command mocking will use :data:`os.defpath` as the initial PATH if the PATH
  environment variable is not set.
