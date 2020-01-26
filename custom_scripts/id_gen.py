#!/usr/local/bin/python3

# JS version
# export default function idGen() {
#     // 1578795600000 = milliseconds from 1970 to Jan 12, 2020
#     let datePart = (new Date().getTime() - 1578795600000).toString();
#     // Up to 4 hex digits
#     let randomPart = (Math.floor(Math.random() * 999998) + 1).toString();
#     randomPart = randomPart.padStart(6, "0");
#     return parseInt(datePart + randomPart);
# }

import time
from random import randrange
from base64_id import base64_id

# Python version
def id_gen():
	# 1578795600000 = milliseconds from 1970 to Jan 12, 2020
	millis_since_1970 = 1578795600000
	millis = int(round(time.time() * 1000)) - millis_since_1970
	# Up to 4 hex digits
	random_part = randrange(999999)
	# Zero pad
	int_id = int(str(millis) + str(random_part).zfill(6))
	# base64 encode
	return base64_id(int_id)