import os
import stat

__all__ = ['assert_path_exists', 'assert_not_path_exists',
           'assert_isfile', 'assert_not_isfile',
           'assert_isdir', 'assert_not_isdir',
           'assert_islink', 'assert_not_islink',
          ]

def _stat_for_assert(path, follow_symlinks=True, msg=None):
    stat = os.stat if follow_symlinks else os.lstat
    try:
        return stat(path)
    except OSError:
        if msg is None:
            msg = "Path does not exist, or can't be stat-ed: %r" % path
        raise AssertionError(msg)

def assert_path_exists(path, msg=None):
    """Assert that something exists at the given path.
    """
    _stat_for_assert(path, True, msg)

def assert_not_path_exists(path, msg=None):
    """Assert that nothing exists at the given path.
    """
    if os.path.exists(path):
        if msg is None:
            msg = "Path exists: %r" % path
        raise AssertionError(msg)

def assert_isfile(path, follow_symlinks=True, msg=None):
    """Assert that path exists and is a regular file.
    
    With follow_symlinks=True, the default, this will pass if path is a symlink
    to a regular file. With follow_symlinks=False, it will fail in that case.
    """
    st = _stat_for_assert(path, follow_symlinks, msg)
    if not stat.S_ISREG(st.st_mode):
        if msg is None:
            msg = "Path exists, but is not a regular file: %r" % path
        raise AssertionError(msg)

def assert_not_isfile(path, follow_symlinks=True, msg=None):
    """Assert that path exists but is not a regular file.
    
    With follow_symlinks=True, the default, this will fail if path is a symlink
    to a regular file. With follow_symlinks=False, it will pass in that case.
    """
    st = _stat_for_assert(path, follow_symlinks, msg)
    if stat.S_ISREG(st.st_mode):
        if msg is None:
            msg = "Path is a regular file: %r" % path
        raise AssertionError(msg)

def assert_isdir(path, follow_symlinks=True, msg=None):
    """Assert that path exists and is a directory.
    
    With follow_symlinks=True, the default, this will pass if path is a symlink
    to a directory. With follow_symlinks=False, it will fail in that case.
    """
    st = _stat_for_assert(path, follow_symlinks, msg)
    if not stat.S_ISDIR(st.st_mode):
        if msg is None:
            msg = "Path exists, but is not a directory: %r" % path
        raise AssertionError(msg)

def assert_not_isdir(path, follow_symlinks=True, msg=None):
    """Assert that path exists but is not a directory.
    
    With follow_symlinks=True, the default, this will fail if path is a symlink
    to a directory. With follow_symlinks=False, it will pass in that case.
    """
    st = _stat_for_assert(path, follow_symlinks, msg)
    if stat.S_ISDIR(st.st_mode):
        if msg is None:
            msg = "Path is a directory: %r" % path
        raise AssertionError(msg)

_link_target_msg = """Symlink target of:
  {path}
Expected:
  {expected}
Actual:
  {actual}
"""

def assert_islink(path, to=None, msg=None):
    """Assert that path exists and is a symlink.
    
    If to is specified, also check that it is the target of the symlink.
    """
    st = _stat_for_assert(path, False, msg)
    if not stat.S_ISLNK(st.st_mode):
        if msg is None:
            msg = "Path exists, but is not a symlink: %r" % path
        raise AssertionError(msg)
    
    if to is not None:
        target = os.readlink(path)
        # TODO: Normalise the target to an absolute path?
        if target != to:
            if msg is None:
                msg = _link_target_msg.format(path=path, expected=to, actual=target)
            raise AssertionError(msg)

def assert_not_islink(path, msg=None):
    """Assert that path exists but is not a symlink.
    """
    st = _stat_for_assert(path, False, msg)
    if stat.S_ISLNK(st.st_mode):
        if msg is None:
            msg = "Path is a symlink: %r" % path
        raise AssertionError(msg)
