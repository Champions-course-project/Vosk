import os
import json
import wave
import vosk_class
import recorder

os.chdir("vosk test")

FN = "file.wav"

try:
    while True:
        input("Нажмите Enter для записи и мгновенного распознавания. Нажмите Ctrl-C для выхода.")

        try:
            print("Запись!")
            result = vosk_class.STT.decode()
            print("Завершение записи.")
            with open("data.json", "w", encoding="UTF-8") as F:
                json.dump(result, F, ensure_ascii=False, indent=4)

            print("Расшифровано слово: {0}".format(result["text"]))

        except FileNotFoundError:
            print("\nОшибка! Файл еще не создан. \nСоздайте файл при помощи другого скрипта и повторите попытку. \nЭто приложение можно не закрывать!\n")

        except Exception as ex:
            print("Необработанное исключение.")
            print("Имя исключения: {0}".format(type(ex).__name__))
            print("Аргументы: {0}".format(ex.args))
            input_string = ""
            while (input_string not in ("0", "1")):
                input_string = input(
                    "Введите 1, чтобы проигнорировать исключение, или 0, чтобы выйти из программы: ")
            if (input_string == "0"):
                raise

except KeyboardInterrupt:
    print("\nВыход из программы...")
    exit()
