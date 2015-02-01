import os
from subprocess import call
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