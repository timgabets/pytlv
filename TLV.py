#!/usr/bin/env python

import binascii
from collections import OrderedDict

class TLV:
	def __init__(self, tags):
		self.tags = tags
		
		self.tag_lengths = set()
		for tag in self.tags:
			self.tag_lengths.add(len(tag))

	def parse(self, tlv_string):
		parsed_data = OrderedDict()

		for i in range(len(tlv_string)):
			for tag_length in self.tag_lengths:
				for tag in self.tags:
					if tlv_string[i:i+tag_length] == tag:
						value_length = int(tlv_string[i+tag_length:i+tag_length+2], 16)
						value = tlv_string[i+tag_length+2 : i+tag_length+2+value_length*2]
						parsed_data[tag] = value

		return parsed_data
