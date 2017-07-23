import wave, pyaudio
import os

# Settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 5

# Record Function
def recordWave():
    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     frames_per_buffer=CHUNK)

    print 'Recording...'

    buffer = []
    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        audio_data = stream.read(CHUNK)
        # check the vad

        buffer.append(audio_data)

    print 'Record Done'

    stream.stop_stream()
    stream.close()
    pa.terminate()

    wf = wave.open('record.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(buffer))
    wf.close()

    # set the data to the asr server
    sentence = os.popen('curl -s -H "Transfer-Encoding:chunked" --data-binary @record.wav http://120.55.182.47:8888/kaldi').read()
    print sentence

if __name__ == '__main__':
    recordWave()
