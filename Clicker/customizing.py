from customFuncs import *

numbers ={
    3:  "Thousand",
    6:  "Million",
    9:  "Billion",
    12: "Trillion",
    15: "Quadrillion",
    18: "Quintillion",
    21: "Sextillion",
    24: "Septillion",
    27: "Octillion",
    30: "Nonillion",
    33: "Decillion",
    36: "Undecillion",
    39: "Duodecillion",
    42: "Tredecillion",
    45: "Quattuordecillion",
    48: "Quindecillion",
    51: "Sexdecillion",
    54: "Septendecillion",
    57: "Octodecillion",
    60: "Novemdecillion",
    63: "Vigintillion"} # between numbers must be exacly the same difference

workers = [ # worker list in format like this: " [name, leveling function, price function, base efficiency, 
            # base price, any function special arguments {"arg": value, "arg2": value}], "
            # when something is None it will be taken from the first worker
    ["test", lv_multiply, price_multiply, 1, 40, {"lv_multiplier": 1.5, "price_multiplier": 3}],
    ["test2", None, None, 20, 100, {"lv_multiplier": 1.7, "price_multiplier": 4}],
    ["cheat(maybe)", None, None, 400, 600, {"lv_multiplier": 3, "price_multiplier": 8}],
]

# click worker in the same format
click_worker = ["test", lv_multiply, price_multiply, 1, 40, {"lv_multiplier": 1.5, "price_multiplier": 3}]
