import unittest
import sys
import mylib

def external_resource_available():
    pass


class MyTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    @unittest.skipIf(mylib.__version__ < (1, 3),
                     "not supported in this library version")
    def test_format(self):
        # Tests that work for only a certain version of the library.
        pass

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_windows_support(self):
        # windows specific testing code
        pass

    def test_maybe_skipped(self):
        if not external_resource_available():
            self.skipTest("external resource not available")
        # test code that depends on the external resource
        pass

class MyFirstTest(unittest.TestCase):

    def test_to_fail(self):
        self.assertTrue(False)

    def test_to_error(self):
        a = 1 / 0
        self.assertTrue(True)

    def test_to_be_ok(self):
        self.assertEqual(2 * 2, 4)

