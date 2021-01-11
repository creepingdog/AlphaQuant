import unittest
import os
from alpha_quant.static import get_project_root


class TestStatic(unittest.TestCase):
    def test_project_root(self):
        self.assertEqual(os.path.basename(get_project_root()), 'alpha_quant')
    #
#


if __name__ == '__main__':
    unittest.main()
#
