import vosk_class


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
    except Exception as exc:
        print(type(exc).__name__)
        print(exc.args)
        return False
