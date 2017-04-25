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
    #def test_tlv_parse_empty_string(self):
    #    self.assertEqual(self.tlv.parse('8C209F02069F03069F1A0295055F2A029A039C019F37049F35019F45029F34039B02'), {})

    def test_tlv_parse_cdol1(self):
        self.assertEqual(self.tlv.parse(''), {})        

    def test_tlv_parse_84_A5(self):
        self.assertEqual(self.tlv.parse('840E315041592E5359532E4444463031A5088801025F2D02656E'), {'84': '315041592E5359532E4444463031', 'A5': '8801025F2D02656E'})

    def test_tlv_parse_nested_tags(self):
        self.assertEqual(self.tlv.parse('84028484A502A5A5'), {'84': '8484', 'A5': 'A5A5'})

    def test_tlv_parse_unknown_tag(self):
        with self.assertRaisesRegex(ValueError, 'Unknown tag found: 9FXX'):
            self.tlv.parse('9FXX')

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
    tlv._parse_tvr()
    """
    def test_tlv_parse_tvr_all_zeros(self):
        self.assertEqual(self.tlv._parse_tvr('0000000000', desc_column_width=48), '')  

    def test_tlv_parse_tvr_byte1_bit8(self):
        self.assertEqual(self.tlv._parse_tvr('8000000000', desc_column_width=48), '\nByte 1: [10000000]\n       Offline data processing was not performed: [1]\n')

    def test_tlv_parse_tvr_byte1_bit7(self):
        self.assertEqual(self.tlv._parse_tvr('4000000000', desc_column_width=48), '\nByte 1: [01000000]\n                                      SDA failed: [1]\n')

    def test_tlv_parse_tvr_byte1_bit6(self):
        self.assertEqual(self.tlv._parse_tvr('2000000000', desc_column_width=48), '\nByte 1: [00100000]\n                                ICC data missing: [1]\n')

    def test_tlv_parse_tvr_byte1_bit5(self):
        self.assertEqual(self.tlv._parse_tvr('1000000000', desc_column_width=48), '\nByte 1: [00010000]\n                  Card number appears on hotlist: [1]\n')

    def test_tlv_parse_tvr_byte1_bit4(self):
        self.assertEqual(self.tlv._parse_tvr('0800000000', desc_column_width=48), '\nByte 1: [00001000]\n                                      DDA failed: [1]\n')

    def test_tlv_parse_tvr_byte1_bit3(self):
        self.assertEqual(self.tlv._parse_tvr('0400000000', desc_column_width=48), '\nByte 1: [00000100]\n                                      CDA failed: [1]\n')

    def test_tlv_parse_tvr_byte1_bit2(self):
        self.assertEqual(self.tlv._parse_tvr('0200000000', desc_column_width=48), '\nByte 1: [00000010]\n                                SDA was selected: [1]\n')

    def test_tlv_parse_tvr_byte1_bit1(self):
        self.assertEqual(self.tlv._parse_tvr('0100000000', desc_column_width=48), '\nByte 1: [00000001]\n                                             RFU: [1]\n')

    def test_tlv_parse_tvr_byte1_bit3_and_bit4(self):
        self.assertEqual(self.tlv._parse_tvr('0C00000000', desc_column_width=48), '\nByte 1: [00001100]\n                                      CDA failed: [1]\n                                      DDA failed: [1]\n')

    def test_tlv_parse_tvr_byte1_bit8_byte2_bit8(self):
        self.assertEqual(self.tlv._parse_tvr('8080000000', desc_column_width=48), '\nByte 1: [10000000]\n       Offline data processing was not performed: [1]\n\nByte 2: [10000000]\nCard and terminal have different application ver: [1]\n')


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


class TestDump(unittest.TestCase):

    def setUp(self):
        self.tlv = TLV()
    
    def test_trace_empty(self):
        self.assertEqual(self.tlv.dump({}), '')

    def test_trace_empty_9f20(self):
        self.assertEqual(self.tlv.dump({'9f02': '000000001337'}), '[9F02] [                    Amount, Authorised (Numeric)]:[000000001337]\n')

    def test_trace_empty_9f20_a5(self):
        self.assertEqual(self.tlv.dump({'9f02': '000000001337', 'a5': '8801025F2D02656E'}), '[9F02] [                    Amount, Authorised (Numeric)]:[000000001337]\n[  A5] [File Control Information (FCI) Proprietary Templ]:[8801025F2D02656E]\n')


if __name__ == '__main__':
    unittest.main()