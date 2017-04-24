#!/usr/bin/env python

import unittest
from TLV import *

class TestTLV(unittest.TestCase):
    def setUp(self):
        self.tlv = TLV(['84', 'A5', '9F02'])

    """
    tlv.parse()
    """
    def test_tlv_parse_empty_string(self):
        self.assertEqual(self.tlv.parse(''), {})

    def test_tlv_parse_84_A5(self):
        self.assertEqual(self.tlv.parse('840E315041592E5359532E4444463031A5088801025F2D02656E'), {'84': '315041592E5359532E4444463031', 'A5': '8801025F2D02656E'})

    def test_tlv_parse_nested_tags(self):
        self.assertEqual(self.tlv.parse('84028484A502A5A5'), {'84': '8484', 'A5': 'A5A5'})   

    def test_tlv_parse_unknown_tag(self):
        with self.assertRaisesRegex(ValueError, 'Unkown tag'):
            self.tlv.parse('9F03')


    """
    tlv.build()
    """
    def test_tlv_build_empty_dict(self):
        self.assertEqual(self.tlv.build({}), '')

    def test_tlv_build_invalid_value_length(self):
        with self.assertRaisesRegex(ValueError, 'Invalid value length - the length must be even'):
            self.tlv.build({'9f02': '123'})

    def test_tlv_build_empty_dict(self):
        self.assertEqual(self.tlv.build({'9f02': '000000001337'}), '9F0206000000001337')


class TestHexify(unittest.TestCase):

    def SetUp(self):
        pass

    def test_hexify_zero(self):
        self.assertEqual(hexify(0), '00')

    def test_hexify_negative(self):
        with self.assertRaisesRegex(ValueError, 'Invalid number to hexify - must be positive'):
            hexify(-3)

    def test_hexify_positive_integer_less_than_16(self):
        self.assertEqual(hexify(12), '0C')

    def test_hexify_255(self):
        self.assertEqual(hexify(255), 'FF')

    def test_hexify_positive_integer_greater_than_256(self):
        self.assertEqual(hexify(730), '02DA')

if __name__ == '__main__':
    unittest.main()