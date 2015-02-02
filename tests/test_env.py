import os
import unittest

import testpath


class EnvironmentUtilsTests(unittest.TestCase):
    def setUp(self):
        # We're actually using this for its specified purpose, rather than
        # explicitly testing it.
        self.addCleanup(testpath.make_env_restorer())

    def test_temporary_env(self):
        os.environ['abc123'] = '4'
        os.environ['def567'] = '8'

        with testpath.temporary_env({'abc123': '9'}):
            self.assertEqual(os.environ['abc123'], '9')
            self.assertNotIn('def567', os.environ)
            os.environ['foo951'] = 'bar'

        self.assertEqual(os.environ['abc123'], '4')
        self.assertEqual(os.environ['def567'], '8')
        self.assertNotIn('foo951', os.environ)

    def test_modified_env(self):
        os.environ['abc123'] = '4'
        os.environ['def567'] = '8'
        os.environ['ghi789'] = '10'
        os.environ.pop('foo951', None)

        with testpath.modified_env({'abc123': '9', 'def567': None}):
            self.assertEqual(os.environ['abc123'], '9')
            self.assertNotIn('def567', os.environ)
            self.assertEqual(os.environ['ghi789'], '10') # Not affected
            os.environ['foo951'] = 'bar'

        self.assertEqual(os.environ['abc123'], '4')
        self.assertEqual(os.environ['def567'], '8')
        self.assertEqual(os.environ['ghi789'], '10') # Not affected
        self.assertNotIn('foo951', os.environ)

    def test_modified_env_nosnapshot(self):
        os.environ['abc123'] = '4'
        os.environ['def567'] = '8'
        os.environ['ghi789'] = '10'
        os.environ.pop('foo951', None)

        with testpath.modified_env({'abc123': '9', 'def567': None}, snapshot=False):
            self.assertEqual(os.environ['abc123'], '9')
            self.assertNotIn('def567', os.environ)
            self.assertEqual(os.environ['ghi789'], '10') # Not affected
            os.environ['foo951'] = 'bar'

        self.assertEqual(os.environ['abc123'], '4')
        self.assertEqual(os.environ['def567'], '8')
        self.assertEqual(os.environ['ghi789'], '10')
        self.assertEqual(os.environ['foo951'], 'bar') # Not reset
