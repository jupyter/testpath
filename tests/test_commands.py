import os
from subprocess import call, check_output
import unittest

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

def test_fixed_output():
    t = 'Sat 24 Apr 17:11:58 BST 2021\n'
    with MockCommand.fixed_output('date', t) as mock_date:
        stdout = check_output(['date'])

    mock_date.assert_called([])
    assert len(mock_date.get_calls()) == 1
    assert stdout.decode('ascii', 'replace') == t
