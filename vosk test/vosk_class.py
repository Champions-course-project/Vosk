from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import json
import recorder
import pprint


class STT:
    # named STT so it can be used instead of SpeechRecognition project
    __model = Model("vosk test\\model")

    @staticmethod
    def decode_bytestream(bytestream: bytes, framerate: int):
        """
        Decode a bytestream using known framerate.\n
        bytestream - simply raw data as a bytes class\n
        framerate - also known as frequency (in Hz)\n
        Returns dictionary, containing words and final result.
        """
        assert type(bytestream) == bytes, "bytestream should be bytes class"
        assert type(framerate) == int, "framerate should be an integer"
        SetLogLevel(0)
        rec = KaldiRecognizer(STT.__model, framerate)
        rec.SetWords(True)
        rec.AcceptWaveform(bytestream)
        result = rec.Result()
        text_to_write = json.loads(result)
        return text_to_write

    @staticmethod
    def decode_file(filename: str):
        """
        Decode data written in .wav file.\n
        filename - name of .wav file (with extencion)\n
        Returns dictionary, containing words and final result.
        """
        assert type(filename) == str, "filename must be string"
        wf = wave.open(filename, "rb")
        result = STT.decode_bytestream(wf.readframes(-1), wf.getframerate())
        wf.close()
        return result

    @staticmethod
    def decode():
        """
        Record data and decode it.\n
        """
        raw_data = recorder.Recorder.record_data()
        return STT.decode_bytestream(raw_data, recorder.Recorder.freq)
