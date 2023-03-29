import pyaudio
import wave


class Recorder:
    # default parameters
    freq = 44100
    __channels = 1
    __FMT = pyaudio.paInt16
    __chunk = 1024
    __rec_len = 4
    output_name = "file.wav"

    # open stream to write into file
    __p = pyaudio.PyAudio()

    @staticmethod
    def record_data():
        """
        Record a raw data and return it.
        """
        NewStream = Recorder.__p.open(rate=Recorder.freq, channels=Recorder.__channels, format=Recorder.__FMT, input=True,
                                      frames_per_buffer=Recorder.__chunk, start=False)
        # record a batch of frames, each 1024 bytes
        frames = []
        NewStream.start_stream()
        for i in range(0, int(Recorder.freq / Recorder.__chunk * Recorder.__rec_len)):
            data = NewStream.read(Recorder.__chunk)
            frames.append(data)
        NewStream.stop_stream()
        NewStream.close()
        raw_data = b''.join(frames)
        return raw_data

    @staticmethod
    def record_file():
        """
        Record file and save it.
        """
        raw_data = Recorder.record_data()
        # write to a .wav file
        wb = wave.open(Recorder.output_name, "wb")
        wb.setnchannels(Recorder.__channels)
        wb.setsampwidth(Recorder.__p.get_sample_size(Recorder.__FMT))
        wb.setframerate(Recorder.freq)
        wb.writeframes(raw_data)
        wb.close()
        return
