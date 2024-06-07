import os
from subprocess import call, check_output
import unittest
import shutil
import sys
import tempfile

from testpath.commands import *

class CommandsTests(unittest.TestCase):
    def test_assert_calls(self):
        initial_path = os.environ['PATH']        
        
        with assert_calls('foobar'):
            call(['foobar'])
        
        with self.assertRaises(AssertionError):
            with assert_calls('foo'):
                pass
        
        # The context manager should clean up $PATH again
        self.assertEqual(os.environ['PATH'], initial_path)
    
    def test_assert_calls_with_args(self):
        with assert_calls('foo', ['bar', 'baz']):
            call(['foo', 'bar', 'baz'])
        
        with self.assertRaises(AssertionError):
            with assert_calls('cheese', ['crackers']):
                call(['cheese', 'biscuits'])
                call(['cheese', 'wine'])

    def test_assert_calls_twice(self):
        with assert_calls('git'):
            call(['git'])

        with self.assertRaises(AssertionError):
            with assert_calls('git'):
                pass

    def test_assert_calls_long_python_path(self):
        current_python = sys.executable
        tmp = tempfile.mkdtemp()
        try:
            tmp_python_dir = tmp
            for _ in range(10):
                tmp_python_dir = os.path.join(tmp_python_dir, 'looooooooooooooooooooooooooooooooooooooooooong_segment')
            os.makedirs(tmp_python_dir)
            tmp_python = os.path.join(tmp_python_dir, 'python')
            os.symlink(sys.executable, tmp_python)
            sys.executable = tmp_python

            with assert_calls('i_dont_exist'):
                call(['i_dont_exist'])
            with assert_calls('git'):
                call(['git'])
        finally:
            sys.executable = current_python
            shutil.rmtree(tmp, ignore_errors=True)

def test_fixed_output():
    t = 'Sat 24 Apr 17:11:58 BST 2021\n'
    with MockCommand.fixed_output('date', t) as mock_date:
        stdout = check_output(['date'])

    mock_date.assert_called([])
    assert len(mock_date.get_calls()) == 1
    assert stdout.decode('ascii', 'replace') == t
