#!/usr/bin/env python

import unittest
from TLV import *

class TestTLV(unittest.TestCase):
    def setUp(self):
        self.tlv = TLV()

    def test_tlv_parse_empty_string(self):
        self.assertEqual(self.tlv.parse(''), None)

if __name__ == '__main__':
    unittest.main()