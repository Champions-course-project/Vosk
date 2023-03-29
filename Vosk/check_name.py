def check(student_name: str, word: str):
    student_name = student_name.lower().replace(
        'ё', 'е').replace(' ', '').replace('-', '')
    word = word.lower().replace('ё', 'е').replace('-', '')

    def full_check(student_name, word):
        if student_name == word:
            return True
        return False

    def part_check(student_name, word):
        # added so some short names cannot throw an exception because of index being out of range
        try:
            if student_name[0:3] == word[0:3]:
                return True
            return False
        except:
            return False

    # should create much more checks than now!!!

    if full_check(student_name, word):
        return 2  # Полное совпадение
    elif part_check(student_name, word):
        return 1  # Частичное совпадение
    return False
