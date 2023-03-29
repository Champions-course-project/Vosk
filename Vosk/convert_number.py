# Переводим из слова в число
def convert_string(string):
    ones = ["один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять", "десять", "одиннадцать",
            "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать",
            "девятнадцать", ]
    tens = ["двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят", "семьдесят", "восемьдесят", "девяносто"]
    hundreds = ["сто", "двести", "триста", "четыреста", "пятьсот", "шестьсот", "семьсот", "восемьсот", "девятьсот"]
    converted = []
    string = string.lower().split(' ')
    for element in string:
        element = element.replace('ё', '')
        if element in ones:
            converted.append(ones.index(element) + 1)
        elif element in tens:
            converted.append((tens.index(element) + 2) * 10)
        elif element in hundreds:
            converted.append((hundreds.index(element) + 1) * 100)
        else:
            return -1
    if converted:
        return sum(converted)
    return -1


def convert_course(string):
    ones_ord = ["первый", "второй", "третий", "четвертый", "пятый", "шестой"]
    string = string.lower().replace('ё', 'е')
    if string in ones_ord:
        return ones_ord.index(string) + 1
    return -1


if __name__ == "__main__":
    print(convert_string("сто"))
    print(convert_course("четвёртый"))