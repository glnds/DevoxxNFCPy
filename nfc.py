#! /usr/bin/env python

from smartcard.System import readers
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.util import toBytes, toHexString
import logging

# Initialize logging.
logging.basicConfig(filename='nfc.log', level=logging.INFO)

# Define the APDUs used in this script
CMD_SERIAL_ID = toBytes("80 14 00 00 08")
CMD_CARD_ID = toBytes("80 14 04 00 06")
CMD_NFC_SCAN = toBytes("ff 00 00 00 06 D4 60 01 01 00 20")
GET_RESPONSE = toBytes("FF C0 00 00 FF")

debug = False

# get all the available readers
readers = readers()
print "Available readers:", readers

reader = readers[0]
print "Using:", reader

connection = reader.createConnection()
connection.connect()

if debug:
    observer = ConsoleCardConnectionObserver()
    connection.addObserver(observer)


# Get the reader's serial id
data, sw1, sw2 = connection.transmit(CMD_SERIAL_ID)
serialId = toHexString(data)
print "Reader's serial id: {}".format(serialId)
logging.info("Reader serial id: %s", serialId)
logging.info("APDU Command result: %02X %02X", sw1, sw2)


# Get the reader's card id
data, sw1, sw2 = connection.transmit(CMD_CARD_ID)
cardId = toHexString(data)
print "Reader's card id: {}".format(cardId)
logging.info("Reader card id: %s", cardId)
logging.info("APDU Command result: %02X %02X", sw1, sw2)


old_tag = []
while True:
    data, sw1, sw2 = connection.transmit(CMD_NFC_SCAN)
    if debug:
        print data
        print "Command: %02X %02X" % (sw1, sw2)

    if sw2 == 5:
        old_tag = []
        continue

    GET_RESPONSE[4] = sw2
    tag, sw1, sw2 = connection.transmit(GET_RESPONSE)
    if debug:
        print tag
        print "Response: %02X %02X" % (sw1, sw2)

    if tag != old_tag:
        old_tag = tag
        print toHexString(tag)
