#!/usr/bin/env python

import unittest
from TLV import *
from collections import OrderedDict


class TestTLVKnownTags(unittest.TestCase):
    def setUp(self):
        self.tlv = TLV()

    """
    tlv.parse()
    """
    def test_tlv_parse_empty_string(self):
        self.assertEqual(self.tlv.parse(''), {})

    #def test_tlv_parse_84_A5(self):
    #    self.assertEqual(self.tlv.parse('820200009A03170424950500000000009F100200009F2608B3336140668238F59F360200019F370472199A459F1A020643'), OrderedDict({'82': '0000', '9A': '170424', '95': '0000000000', '9F10': '0000', '9F26': 'B3336140668238F5', '9F36': '0001', '9F37': '72199A45', '9F1A': '0643'}))

    #def test_tlv_parse_84_A5(self):
    #    self.assertEqual(self.tlv.parse('820200009A0317042495050000000000'), OrderedDict({'82': '0000', '9A': '170424', '95': '0000000000'}))


class TestTLVCustomTagsList(unittest.TestCase):
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
        with self.assertRaisesRegex(ValueError, 'Unknown tag found: 9F03'):
            self.tlv.parse('9F03')

    def test_tlv_parse_known_tag_no_length_no_value(self):
        with self.assertRaisesRegex(ValueError, 'Parse error: tag 9F02 has incorrect data length'):
            self.tlv.parse('9F02')

    def test_tlv_parse_known_tag_no_length_0(self):
        with self.assertRaisesRegex(ValueError, 'Parse error: tag 9F02 declared data of length 4, but actual data length is 0'):
            self.tlv.parse('9F0204')

    def test_tlv_parse_known_tag_no_length_2(self):
        with self.assertRaisesRegex(ValueError, 'Parse error: tag 9F02 declared data of length 4, but actual data length is 2'):
            self.tlv.parse('9F02040102')

    def test_tlv_parse_known_tag_no_length_4(self):
        with self.assertRaisesRegex(ValueError, 'Parse error: tag 9F02 declared data of length 4, but actual data length is 3'):
            self.tlv.parse('9F0204010203')

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

    def test_tlv_build_tag_with_empty_data(self):
        self.assertEqual(self.tlv.build({'9f02': ''}), '')

    def test_tlv_build_tag_without_data(self):
        self.assertEqual(self.tlv.build({'9f02': None}), '')


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