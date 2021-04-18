from typing import List
import string

def convert_to_superscript(input) -> str:
    """ Convert string to superscript string """

    string = str(input)
    # sup = string.maketrans("1234567890()", chr(0x00b9) + chr(0x00B2) + chr(
    #                 0x00B3) + u"\u2074" + u"\u2075" + u"\u2076" + u"\u2077" + u"\u2078" + u"\u2079" + u"\u2070" +u"\u207D" +u"\u207E")

    superscript_map = {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
        "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
        "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
        "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
        "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
        "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
        "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
        "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
        "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
        "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"}

    trans = str.maketrans(
        ''.join(superscript_map.keys()),
        ''.join(superscript_map.values()))

    return string.translate(trans)


def convert_number_to_letters(input : int) -> str:
    """ Convert numbers to letters, e.g. 1 to 'a' or 137 to 'eg' """

    def number_to_letter(number: int) -> str:
        if number == 0: return ''
        return chr(ord('`')+number)

    quotient, remainder = divmod(input,26)
    output = f'{number_to_letter(quotient)}{number_to_letter(remainder)}'

    return output


def convert_number_to_footnote(input: int) -> str:
    """ Convert number to a footnote """

    if input == 0: return ''

    return convert_to_superscript(convert_number_to_letters(input))
