
TLV parser

 from pytlv import *

 tlv = TLV(['84', 'A5'])
 tlv.parse('840E315041592E5359532E4444463031A5088801025F2D02656E')

>>> [['tag': '84', length: '0E', value: '315041592E5359532E4444463031'], ['tag': 'A5', length: '08', 'value': '8801025F2D02656E']]