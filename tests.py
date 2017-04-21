#!/usr/bin/env python

import unittest
from TLV import *

class TestTLV(unittest.TestCase):
    def setUp(self):
        self.tlv = TLV(['84', 'A5', '9F02'])

    def test_tlv_parse_empty_string(self):
        self.assertEqual(self.tlv.parse(''), {})

    def test_tlv_parse_84_A5(self):
        self.assertEqual(self.tlv.parse('840E315041592E5359532E4444463031A5088801025F2D02656E'), {'84': '315041592E5359532E4444463031', 'A5': '8801025F2D02656E'})

    def test_tlv_parse_nested_tags(self):
        self.assertEqual(self.tlv.parse('84028484A502A5A5'), {'84': '8484', 'A5': 'A5A5'})   

    def test_tlv_parse_unknown_tag(self):
        with self.assertRaisesRegex(ValueError, 'Unkown tag'):
            self.tlv.parse('9F03')



if __name__ == '__main__':
    unittest.main()