import os
import json
import vosk_class
import recorder
import vosk_functions

os.chdir("Vosk")

FN = "file.wav"

while True:
    try:
        while True:
            input(
                "Нажмите Enter для записи и мгновенного распознавания. Нажмите Ctrl-C для выхода.")

            try:
                print("Запись!")
                bytestream = recorder.Recorder.record_data()
                print("Завершение записи.")
                result = vosk_class.STT.decode_bytestream(
                    bytestream, recorder.Recorder.freq)
                with open("data.json", "w", encoding="UTF-8") as F:
                    json.dump(result, F, ensure_ascii=False, indent=4)

                print("Расшифровано слово: {0}".format(result["text"]))
                print("Расшифровка от speech: {0}".format(
                    vosk_functions.speech(bytestream, recorder.Recorder.freq)))

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
        try:
            while True:
                n = input(
                    "\nВы хотите выйти из программы или перезапустить модель? (1 = выйти из программы, 2 = перезапустить) ")
                if n == "1":
                    print("Выход из программы...")
                    exit()
                elif n == "2":
                    break
                else:
                    print("Некорректный ввод. Повторите попытку.")
        except KeyboardInterrupt:
            print("\nВыход из программы...")
            exit()
