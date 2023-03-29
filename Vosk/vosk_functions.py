import Vosk.vosk_class as vosk_class
from .check_name import check
import os
import json
import Vosk.convert_number as convert_number


def speech(bytes_array: bytes, framerate: int):
    """
    Распознаватель речи.\n
    Входные аргументы:
    - bytes_array - байтовый поток с аудиоинформацией;
    - framerate - частота записи.\n
    Выходные данные:
    - список возможных словосочетаний - при успешном распознавании;
    - False - при ошибке во время распознавания.
    """
    try:
        result = vosk_class.STT.decode_bytestream(bytes_array, framerate)
        if result:
            word = result["text"].replace("!SIL", "")
            if word == "":
                return []
            return [word]
        else:
            return False
    except Exception as ex:
        print(type(ex).__name__)
        print(ex.args)
        return False


def get_faculty(bytestream: bytes, framerate: int):
    """
    Распознаватель факультета на основе имеющегося списка.\n
    Входные аргументы:
    - bytes_array - байтовый поток с аудиоинформацией;
    - framerate - частота записи.\n
    Выходные данные:
    - пара "число - название факультета" в случае успеха;
    - пара False - False в противном случае.
    """
    with open(os.path.join("Vosk", "pnu_info", "Факультеты и институты.json"), 'r', encoding='UTF-8') as file:
        faculties_dict = json.load(file)

    # Отображение факультетов и институтов
    faculties_list = list(faculties_dict.keys())

    # цикл выбора факультета
    try:
        words_list = speech(bytestream, framerate)
        if words_list:
            number = words_list[0]
            if not words_list[0].isdigit():
                number = convert_number.convert_string(number)
            number = int(number)
            return number, faculties_list[number - 1]
        else:
            return False, False
    except Exception as exc:
        print(type(exc).__name__)
        print(exc.args)
        return False, False


def get_course(faculty: str, bytestream: bytes, framerate: int):
    """
    Распознаватель номера курса на основе имеющегося списка.\n
    Входные аргументы:
    - bytes_array - байтовый поток с аудиоинформацией;
    - framerate - частота записи;
    - faculty - наименование факультета в списке.\n
    Выходные данные:
    - число, соответствующее номеру курса в случае успеха;
    - False в противном случае.
    """
    with open(os.path.join("Vosk", "pnu_info", "groups_info.json"), 'r', encoding='UTF-8') as file:
        groups_dict = json.load(file)
    courses_list = []
    for course_number in groups_dict[faculty].keys():
        courses_list.append(course_number)

    try:
        words_list = speech(bytestream, framerate)
        if words_list:
            course = words_list[0]
            if not words_list[0].isdigit():
                course = convert_number.convert_course(course)
            assert str(course) + " курс" in courses_list
            course = int(course)
            return course
        else:
            return False
    except Exception as exc:
        print(type(exc).__name__)
        print(exc.args)
        return False


def get_group(faculty: str, course: int, bytestream: bytes, framerate: int):
    """
    Распознаватель произнесенного номера группы на основе списка групп.\n
    Входные аргументы:
    - bytes_array - байтовый поток с аудиоинформацией;
    - framerate - частота записи;
    - faculty - наименование факультета в списке;
    - course - порядковый номер курса.\n
    Выходные данные:
    - номер группы в списке групп в случае успеха;
    - False в противном случае.
    """
    with open(os.path.join("Vosk", "pnu_info", "groups_info.json"), 'r', encoding='UTF-8') as file:
        groups_dict = json.load(file)
    groups_list = groups_dict[faculty].get(str(course) + ' курс')
    if groups_list:
        try:
            words_list = speech(bytestream, framerate)
            if words_list:
                group = words_list[0]
                if not words_list[0].isdigit():
                    group = convert_number.convert_string(group)
                group = int(group)
                assert group > 0 and group <= len(groups_list)
                return group
            else:
                return False
        except Exception as exc:
            print(type(exc).__name__)
            print(exc.args)
            return False
    else:
        return False


def get_date(bytestream: bytes, framerate: int):
    """
    Распознаватель произнесённой даты.\n
    Входные аргументы:
    - bytes_array - байтовый поток с аудиоинформацией;
    - framerate - частота записи.\n
    Выходные данные:
    - дата в формате ДД.ММ.ГГГГ в случае успеха;
    - False в противном случае.
    """
    words_list = speech(bytestream, framerate)

    if words_list:

        days_list = [
            'первое', 'второе', 'третье', 'четвертое',
            'пятое', 'шестое', 'седьмое', 'восьмое',
            'девятое', 'десятое', 'одиннадцатое', 'двенадцатое',
            'тринадцатое', 'четырнадцатое', 'пятнадцатое', 'шестнадцатое',
            'семнадцатое', 'восемнадцатое', 'девятнадцатое', 'двадцатое',
            'двадцать первое', 'двадцать второе', 'двадцать третье',
            'двадацать четвертое', 'двадцать пятое', 'двадцать шестое',
            'двадцать седьмое', 'двадцать восьмое', 'двадцать девятое',
            'тридцатое', 'тридцать первое'
        ]
        months_list = [
            'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
        ]
        # Список дат из журнала
        dates_list = []
        with open(os.path.join("Vosk", "Dates.txt"), 'r', encoding='UTF-8') as F:
            for date in F:
                dates_list.append(date.replace("\n", ""))

        date = ""
        for string in words_list:
            month = string.split(' ')[-1]
            if month.lower() in months_list:

                # создание номера месяца
                month = str(months_list.index(month) + 1)
                if len(month) == 1:
                    month = "0" + month

                string = string.split(' ')[:-1]
                # возврат числа
                if string[0].isdigit():
                    # если вернул число - дополняет его до даты
                    if len(string[0]) == 1:
                        day = "0" + string[0]
                    else:
                        day = string[0]
                    date = f"{day}.{month}."
                    # !!! Внимание на "2023" - это затычка
                    if date + "2023" in dates_list:
                        return date
                    print(f"Такой даты нет в журнале! | {date}2023")
                    return False

                # если слово "первое", "второе", ..., но не "двадцать первое"
                elif len(string) == 1:
                    day = string[0].lower().replace('ё', 'е')
                    if day in days_list:
                        # конвертировали в день
                        day = str(days_list.index(day) + 1)
                        if len(day) == 1:
                            day = "0" + day
                        date = f"{day}.{month}."
                        if date + "2023" in dates_list:
                            return date
                        else:
                            print(f"Такой даты нет в журнале! | {date}2023")
                            return False
                    print("Распознавание даты не прошло!")
                    return False

                # если слова "двадцать первое", "двадцать второе", ...
                elif len(string) == 2:
                    for element in string:
                        date += element.lower().replace('ё', 'е') + " "
                    if date[:-1] in days_list:
                        date = str(days_list.index(date[:-1]) + 1)
                        date = date + "." + month + "."
                        # !!! Внимание на "2023" - это затычка
                        if date + "2023" in dates_list:
                            return date
                        else:
                            print(f"Такой даты нет в журнале! | {date}2023")
                            return False
                    print("Распознавание даты не прошло!")
                    return False
    print("Не молчите в микрофон!")
    return False


def get_student_name(students_list: list[str], bytestream: bytes, framerate: int):
    """
    Распознаватель произнесенных фамилий.\n
    Входные аргументы:
    - bytes_array - байтовый поток с аудиоинформацией;
    - framerate - частота записи;
    - students_list - список студентов с именами в формате:
    Фамилия Имя Отчество.\n
    Выходные данные:
    - ФИО студента в случае успешного распознавания и совпадения;
    - False в противном случае.
    """
    words_list = speech(bytestream, framerate)

    if words_list:

        # распознавание фамилий: полное или частичное
        possible_names_list = set()
        definite_names_list = set()
        for student_name in students_list:

            for word in words_list:

                status = check(student_name.split(" ")[0], word)

                if status == 2:
                    definite_names_list.add(student_name)
                elif status == 1:
                    possible_names_list.add(student_name)

        if definite_names_list:
            if len(definite_names_list) == 1:
                return (str)((list)(definite_names_list)[0])
            return False

        elif possible_names_list:
            if len(possible_names_list) == 1:
                return (str)((list)(possible_names_list)[0])
            return False

        print("Распознавание не прошло! Попробуйте еще раз!")
        return False
    print("Не молчите в микрофон!")
    return False


def get_status(bytestream: bytes, framerate: int):
    """
    Распознаватель произнесенных оценок и статусов студентов.\n
    Входные аргументы:
    - bytes_array - байтовый поток с аудиоинформацией;
    - framerate - частота записи.\n
    Выходные данные:
    - строка, указывающая на состояние, в случае успеха;
    - False в противном случае.
    """
    words_list = speech(bytestream, framerate)

    if words_list:
        excellent_list = ['отлично', 'пять', 'пятерка']
        good_list = ['хорошо', 'четыре', 'четверка']
        satisfactory_list = ['удовлетворительно', 'три', 'тройка']
        bad_list = ['неудовлетворительно', 'два', 'двойка']
        absent_list = ['неявка', 'отсутствие', 'отсутствует']
        present_list = ['явка', 'присутствие', 'присутствует']
        reason_list = ['болеет', 'причина']
        exam_good_list = ['зачёт', 'зачет', 'зачтено']
        exam_bad_list = ['незачёт', 'незачет', 'не зачтено']
        status = words_list[0]
        if status in excellent_list:
            return "Отлично"
        elif status in good_list:
            return "Хорошо"
        elif status in satisfactory_list:
            return "Удовл."
        elif status in bad_list:
            return "Неудовл."
        elif status in absent_list:
            return "Неявка"
        elif status in present_list:
            return "Явка"
        elif status in reason_list:
            return "Болеет"
        elif status in exam_good_list:
            return "Зачёт"
        elif status in exam_bad_list:
            return "Незачёт"
    print("Попробуйте еще раз!")
    return False
