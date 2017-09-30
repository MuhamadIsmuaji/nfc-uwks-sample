from smartcard.scard import *
from smartcard.util import toHexString
from smartcard.util import toASCIIString
import smartcard.util
from smartcard.ATR import ATR
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnectionObserver import CardConnectionObserver
import time
import struct
import array

import json as simplejson
import sys
'''
RFID/NFC Reader/Writer: ACR122U-A9
Supported Frequency: 13.56MHz
Supported ISO: 14443-4A/B, ISO 18092.
Additional Supported Standards: Mifare, FeliCa, four types of NFC.
Documentation: http://downloads.acs.com.hk/drivers/en/API-ACR122U-2.02.pdf


Definitions:
ISO/IEC 14443 Identification cards -- Contactless integrated circuit cards -- Proximity cards is an international standard that defines proximity cards used for identification, and the transmission protocols for communicating with it.
(ATR) Answer To Reset: is a message output by a contact Smart Card conforming to ISO/IEC 7816 standards, following electrical reset of the card's chip by a card reader.
PCD: proximity coupling device (the card reader)
PICC: proximity integrated circuit card


'''
VERBOSE = False

attributes = {
	SCARD_ATTR_ATR_STRING: 'SCARD_ATTR_ATR_STRING',
	SCARD_ATTR_CHANNEL_ID: 'SCARD_ATTR_CHANNEL_ID',
	SCARD_ATTR_CHARACTERISTICS: 'SCARD_ATTR_CHARACTERISTICS',
	SCARD_ATTR_CURRENT_BWT: 'SCARD_ATTR_CURRENT_BWT',
	SCARD_ATTR_CURRENT_CWT: 'SCARD_ATTR_CURRENT_CWT',
	SCARD_ATTR_CURRENT_EBC_ENCODING: 'SCARD_ATTR_CURRENT_EBC_ENCODING',
	SCARD_ATTR_CURRENT_F: 'SCARD_ATTR_CURRENT_F',
	SCARD_ATTR_CURRENT_IFSC: 'SCARD_ATTR_CURRENT_IFSC',
	SCARD_ATTR_CURRENT_IFSD: 'SCARD_ATTR_CURRENT_IFSD',
	SCARD_ATTR_CURRENT_IO_STATE: 'SCARD_ATTR_CURRENT_IO_STATE',
	SCARD_ATTR_DEFAULT_DATA_RATE: 'SCARD_ATTR_DEFAULT_DATA_RATE',
	SCARD_ATTR_DEVICE_FRIENDLY_NAME_A: 'SCARD_ATTR_DEVICE_FRIENDLY_NAME_A',
	SCARD_ATTR_DEVICE_FRIENDLY_NAME_W: 'SCARD_ATTR_DEVICE_FRIENDLY_NAME_W',
	SCARD_ATTR_DEVICE_SYSTEM_NAME_A: 'SCARD_ATTR_DEVICE_SYSTEM_NAME_A',
	SCARD_ATTR_DEVICE_SYSTEM_NAME_W: 'SCARD_ATTR_DEVICE_SYSTEM_NAME_W',
	SCARD_ATTR_DEVICE_UNIT: 'SCARD_ATTR_DEVICE_UNIT',
	SCARD_ATTR_ESC_AUTHREQUEST: 'SCARD_ATTR_ESC_AUTHREQUEST',
	SCARD_ATTR_EXTENDED_BWT: 'SCARD_ATTR_EXTENDED_BWT',
	SCARD_ATTR_ICC_INTERFACE_STATUS: 'SCARD_ATTR_ICC_INTERFACE_STATUS',
	SCARD_ATTR_ICC_PRESENCE: 'SCARD_ATTR_ICC_PRESENCE',
	SCARD_ATTR_ICC_TYPE_PER_ATR: 'SCARD_ATTR_ICC_TYPE_PER_ATR',
	SCARD_ATTR_MAXINPUT: 'SCARD_ATTR_MAXINPUT',
	SCARD_ATTR_MAX_CLK: 'SCARD_ATTR_MAX_CLK',
	SCARD_ATTR_MAX_DATA_RATE: 'SCARD_ATTR_MAX_DATA_RATE',
	SCARD_ATTR_POWER_MGMT_SUPPORT: 'SCARD_ATTR_POWER_MGMT_SUPPORT',
	SCARD_ATTR_SUPRESS_T1_IFS_REQUEST: 'SCARD_ATTR_SUPRESS_T1_IFS_REQUEST',
	SCARD_ATTR_USER_AUTH_INPUT_DEVICE: 'SCARD_ATTR_USER_AUTH_INPUT_DEVICE',
	SCARD_ATTR_USER_TO_CARD_AUTH_DEVICE:
		'SCARD_ATTR_USER_TO_CARD_AUTH_DEVICE',
	SCARD_ATTR_VENDOR_IFD_SERIAL_NO: 'SCARD_ATTR_VENDOR_IFD_SERIAL_NO',
	SCARD_ATTR_VENDOR_IFD_TYPE: 'SCARD_ATTR_VENDOR_IFD_TYPE',
	SCARD_ATTR_VENDOR_IFD_VERSION: 'SCARD_ATTR_VENDOR_IFD_VERSION',
	SCARD_ATTR_VENDOR_NAME: 'SCARD_ATTR_VENDOR_NAME',
}

NUMBER_BYTES_TO_UPDATE = 0x10

READER_STATUS = 0
CARD_STATUS = 0;

SECTOR = 6
BLOCK = 25
LENGTH = 1

AUTHENTICATE = [0xFF, 0x88, 0x00, BLOCK, 0x60, 0x00]
UPDATE_FIXED_BLOCKS = [0xFF, 0xD6, 0x00, BLOCK, NUMBER_BYTES_TO_UPDATE]
		
COMMAND_READ_AUTH = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, SECTOR*4, 0x60, 0x00]
COMMAND_READ = [0xFF, 0xB0, 0x00, BLOCK, LENGTH]

class NFC_Reader():


	def __init__(self, uid = ""):
		self.uid = uid
		self.hresult, self.hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
		self.hresult, self.readers = SCardListReaders(self.hcontext, [])
		# bug test python
		# assert len(self.readers) > 0
		
		if len(self.readers) > 0:
			self.READER_STATUS = 1
			self.reader = self.readers[0]

		else :
			self.READER_STATUS = 0;

	def get_reader_status(self):
		return self.READER_STATUS

	def get_card_status(self):

		self.hresult, self.hcard, self.dwActiveProtocol = SCardConnect(
					self.hcontext,
					self.reader,
					SCARD_SHARE_SHARED,
					SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
		self.data_blocks = []

		
		if self.hcard == 0 :
			return 0
		else :
			return 1

	def send_command(self, command):
		# print("Sending command...")
		for iteration in range(1):
			try:
				self.hresult, self.response = SCardTransmit(self.hcard,self.dwActiveProtocol,command)
				value = toHexString(self.response, format=0)
				if(VERBOSE):
					print("Value: " + value +  " , Response:  " + str(self.response) + " HResult: " + str(self.hresult))
			except SystemError:
				print ("No Card Found")
			time.sleep(1)
		# print("------------------------\n")
		return self.response, value

	def write_card(self, string):

		int_array = map(ord, string)

		# If the string is greater than 16 characters, break. 
		if(len(int_array) > 16):
			return

		# Add the converted string to hex blocks to the APDU command.
		for value in int_array:
			i = 0

			if i == 0 :
				UPDATE_FIXED_BLOCKS.append(value)

			i = i + 1

		for value in range(2,16) :
			UPDATE_FIXED_BLOCKS.append(0x00)
		
		# Authenticate with the specified block with the APDU authenticate command.
		response, value = self.send_command(AUTHENTICATE)

		# print("Writing " + string + " to card...")
		if(response == [144, 0]):
			# print("Authentication successful.")

			if(len(string) > 0):
				# print("Writing data blocks...")
				self.send_command(UPDATE_FIXED_BLOCKS)
				write_status = "Berhasil."
			else:
				write_status = "String tidak valid."

		else:
			write_status = "Autentikasi gagal."

		return write_status



if __name__ == '__main__':

	reader = NFC_Reader()

	reader_status = reader.get_reader_status()

	if reader_status != 1 :
		data = simplejson.dumps({"status": "0", "message" : "Reader not detected", "write" : "0"})
	else :
		data = simplejson.dumps({"status": "1", "message" : "Reader detected", "write" : "0", "write" : "0"})

		card_status = reader.get_card_status()

		if card_status != 1 :
			data = simplejson.dumps({"status": "0", "message" : "Reader detected, but card not detected", "write" : "0"})
		else :
			return_data = reader.write_card(sys.argv[1])
			data = simplejson.dumps({"status": "1", "message" : "Reader and card detected", "write" : return_data})
		

	print data

