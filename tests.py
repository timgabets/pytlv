#!/usr/bin/env python

import unittest
from TLV import *

class TestTLV(unittest.TestCase):
    def setUp(self):
        self.tlv = TLV(['84', 'A5'])

    def test_tlv_parse_empty_string(self):
        self.assertEqual(self.tlv.parse(''), {})

    def test_tlv_parse_84_A5(self):
        self.assertEqual(self.tlv.parse('840E315041592E5359532E4444463031A5088801025F2D02656E'), {'84': '315041592E5359532E4444463031', 'A5': '8801025F2D02656E'})        

if __name__ == '__main__':
    unittest.main()