from customizing import numbers

def nameNumber(num):
    if len(str(num)) < 4:
        return str(num)
    i = 0
    indent = len(str(num)) % 3
    if indent == 0:
        indent = 3
    nzeros = len(str(num)) - indent
    num = f"{str(num)[:indent]}.{str(num)[indent:indent + 1]}"
    while nzeros > 63:
        i += 1
        nzeros -= 63
    return str(num) + " " + numbers[nzeros] + (" Vigintillions " * i)
