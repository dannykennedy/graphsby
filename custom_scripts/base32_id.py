#!/usr/local/bin/python3

# Based on https://gist.github.com/alkaruno/b84162bae5115f4ca99b

import math

def base32_id(value):
    ALPHA = "abcdefghijklmnopqrstuvwxyz234567";

    result = ""
    while True:
        mod = value % 32;
        result = ALPHA[mod] + result;
        value = math.floor(value / 32);
        if (value == 0):
            break

    return result