import os
import unittest

try:
    import pathlib
except ImportError:
    # Python 2 backport
    import pathlib2 as pathlib

from testpath.asserts import *
from testpath.tempdir import TemporaryDirectory

class TestAssertFunctions(unittest.TestCase):
    def setUp(self):
        self.td = TemporaryDirectory()
        self.addCleanup(self.td.cleanup)
        
        self.file_path = os.path.join(self.td.name, 'afile')
        with open(self.file_path, 'w') as f:
            f.write('Blah')
        
        self.dir_path = os.path.join(self.td.name, 'adir')
        os.mkdir(self.dir_path)
        
        self.link_path = os.path.join(self.td.name, 'alink')
        if os.name == 'posix':
            # Symlinks are rarely usable on Windows, because a special
            # permission is needed to create them.
            os.symlink(self.file_path, self.link_path)
        
        self.nonexistant_path = os.path.join(self.td.name, 'doesntexist')
    
    def test_exists(self):
        assert_path_exists(self.file_path)
        assert_path_exists(pathlib.Path(self.file_path))
        assert_not_path_exists(self.nonexistant_path)
        
        with self.assertRaises(AssertionError):
            assert_path_exists(self.nonexistant_path)
        
        with self.assertRaises(AssertionError):
            assert_not_path_exists(self.file_path)
    
    def test_isfile(self):
        assert_isfile(self.file_path)
        assert_not_isfile(self.dir_path)
        
        with self.assertRaises(AssertionError):
            assert_isfile(self.dir_path)
    
        with self.assertRaises(AssertionError):
            assert_not_isfile(self.file_path)

    def test_isfile_symlink(self):
        if os.name == 'nt':
            raise unittest.SkipTest('symlink')
        assert_isfile(self.link_path)  # Follows the link by default
        assert_not_isfile(self.link_path, follow_symlinks=False)

        with self.assertRaises(AssertionError):
            assert_isfile(self.link_path, follow_symlinks=False)
        
        with self.assertRaises(AssertionError):
            assert_not_isfile(self.link_path)

    def test_isdir(self):
        assert_isdir(self.dir_path)
        assert_isdir(pathlib.Path(self.dir_path))
        assert_not_isdir(self.file_path)
        
        with self.assertRaises(AssertionError):
            assert_isdir(self.file_path)
        
        with self.assertRaises(AssertionError):
            assert_not_isdir(self.dir_path)

    def test_islink(self):
        if os.name == 'nt':
            raise unittest.SkipTest('symlink')
        assert_islink(self.link_path, to=self.file_path)
        assert_islink(pathlib.Path(self.link_path),
                      to=pathlib.Path(self.file_path))
        assert_not_islink(self.file_path)
        
        with self.assertRaises(AssertionError) as c:
            assert_islink(self.file_path)
        self.assertIn('not a symlink', str(c.exception))
        
        with self.assertRaises(AssertionError) as c:
            assert_islink(self.link_path, to=self.dir_path)
        self.assertIn('target of', str(c.exception))
        
        with self.assertRaises(AssertionError):
            assert_not_islink(self.link_path)
