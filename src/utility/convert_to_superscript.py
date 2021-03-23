def convert_to_superscript(input):
    string = str(input)
    sup = string.maketrans("1234567890()", chr(0x00b9) + chr(0x00B2) + chr(
                    0x00B3) + u"\u2074" + u"\u2075" + u"\u2076" + u"\u2077" + u"\u2078" + u"\u2079" + u"\u2070" +u"\u207D" +u"\u207E")
    return string.translate(sup)