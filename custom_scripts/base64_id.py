#!/usr/local/bin/python3

# Based on https://gist.github.com/alkaruno/b84162bae5115f4ca99b

import math

def base64_id(value):
    ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-";

    result = ""
    while True:
        mod = value % 64;
        result = ALPHA[mod] + result;
        value = math.floor(value / 64);
        if (value == 0):
            break

    return result




# // https://gist.github.com/alkaruno/b84162bae5115f4ca99b
# // USAGE:
# // var base64 = new Base64();
# // var s = base64.encode(1234567890); // BJlgLS
# // var n = base64.decode('BJlgLS'); // 1234567890
# export var Base64 = (function() {
#     var ALPHA =
#         "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-";

#     var Base64 = function() {};

#     var _encode = function(value) {
#         if (typeof value !== "number") {
#             throw Error("Value is not number!");
#         }

#         var result = "",
#             mod;
#         do {
#             mod = value % 64;
#             result = ALPHA.charAt(mod) + result;
#             value = Math.floor(value / 64);
#         } while (value > 0);

#         return result;
#     };

#     var _decode = function(value) {
#         var result = 0;
#         for (var i = 0, len = value.length; i < len; i++) {
#             result *= 64;
#             result += ALPHA.indexOf(value[i]);
#         }

#         return result;
#     };

#     Base64.prototype = {
#         constructor: Base64,
#         encode: _encode,
#         decode: _decode,
#     };

#     return Base64;
# })();