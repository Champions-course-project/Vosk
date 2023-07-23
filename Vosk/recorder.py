import pyaudio
import wave


class Recorder:
    # default parameters
    freq = 44100
    __channels = 1
    __FMT = pyaudio.paInt16
    __chunk = 1024
    __target_rec_len = 4
    __rec_len = 2
    output_name = "file.wav"

    # open stream to write into file
    __p = pyaudio.PyAudio()

    __NewStream = __p.open(rate=freq, channels=__channels, format=__FMT, input=True,
                           frames_per_buffer=__chunk, start=False)

    @staticmethod
    def record_data():
        """
        Record a raw data and return it.
        """
        # record a batch of frames, each 1024 bytes
        frames = []
        Recorder.__NewStream.start_stream()
        for i in range(0, int(Recorder.freq / Recorder.__chunk * Recorder.__rec_len) + 1):
            data = Recorder.__NewStream.read(Recorder.__chunk)
            frames.append(data)
        Recorder.__NewStream.stop_stream()
        raw_data = b''.join(frames)
        # get the difference in lengths
        add_rec_len = Recorder.__target_rec_len - Recorder.__rec_len
        if add_rec_len > 0:
            # Work with bytes here.
            # Step 1. Get the length required by the each side
            half_add_rec_len = add_rec_len / 2
            # Step 2. Create a bytes fragment. This one will be the same as finishing one.
            additional_bytes = b'\x00' * int(Recorder.__channels * pyaudio.get_sample_size(
                Recorder.__FMT) * Recorder.freq * half_add_rec_len)
            if len(additional_bytes) % 2 != 0:
                additional_bytes += b'\x00'
            # Step 3. join all of the pieces together.
            raw_data = b''.join([additional_bytes, raw_data, additional_bytes])
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

    def __del__(self):
        self.__NewStream.close()
        return
