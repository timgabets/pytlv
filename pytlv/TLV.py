#!/usr/bin/env python

import binascii
from collections import OrderedDict

known_tags = ['8A', '95', '9A', '9F10', '9F26', '9F36']

def hexify(number):
	"""
	Convert integer to hex string representation, e.g. 12 to '0C'
	"""
	if number < 0:
		raise ValueError('Invalid number to hexify - must be positive')

	result = hex(int(number)).replace('0x', '').upper()
	if divmod(len(result), 2)[1] == 1:
		# Padding
		result = '0{}'.format(result)
	return result


class TLV:

	def __init__(self, tags=None):
		if tags:
			self.tags = tags
		else:
			self.tags = known_tags
		self.tlv_string = ''
		
		self.tag_lengths = set()
		for tag in self.tags:
			self.tag_lengths.add(len(tag))


	def parse(self, tlv_string):
		"""
		"""
		parsed_data = OrderedDict()
		self.tlv_string = tlv_string

		i = 0
		while i < len(self.tlv_string): 
			tag_found = False

			for tag_length in self.tag_lengths:
				for tag in self.tags:
					if self.tlv_string[i:i+tag_length] == tag:
						try:
							value_length = int(self.tlv_string[i+tag_length:i+tag_length+2], 16)
						except ValueError:
							raise ValueError('Parse error: tag ' + tag + ' has incorrect data length')

						value_start_position = i+tag_length+2
						value_end_position = i+tag_length+2+value_length*2

						value = self.tlv_string[value_start_position:value_end_position]
						parsed_data[tag] = value

						i = value_end_position
						tag_found = True

			if not tag_found:
				possible_tags = []
				for tag_length in self.tag_lengths:
					possible_tags.append(self.tlv_string[i:i+tag_length])
				msg = 'Unkown tag' + str(possible_tags)
				raise ValueError('Unkown tag')
		return parsed_data


	def build(self, data_dict):
		"""
		"""
		self.tlv_string = ''
		for tag, value in data_dict.items():
			if not value:
				return self.tlv_string

			if divmod(len(value), 2)[1] == 1:
				raise ValueError('Invalid value length - the length must be even')

			self.tlv_string = self.tlv_string + tag.upper() + hexify(len(value) / 2) + value.upper()

		return self.tlv_string
