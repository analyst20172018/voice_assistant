import numpy as np
import io
import logging
import sounddevice
from scipy.io.wavfile import write
import time
from pydub import AudioSegment
import winaudio
from voice_assistant_basic import VoiceAssistantBasic


class VoiceAssistantPC(VoiceAssistantBasic):
    """
        The VoiceAssistantPC class extends VoiceAssistantBasic and provides a PC-based implementation of a voice assistant that
        can communicate with users through a microphone and speakers, convert speech to text, text to speech, and generate
        responses using OpenAI's GPT-4 model.

        Attributes:
            logger (logging.Logger): The logger object for the VoiceAssistantPC.

        Methods:
            record_voice_from_microphone(record_duration_sec): Records voice from the microphone for a specified duration and
                                                            returns a BytesIO stream of the recorded sound.
            
            ask_question(record_duration_sec): Records voice from the microphone, converts it to text, and returns the question text.
            
            play_mp3(mp3_bytes): Plays the given MP3 audio bytes using the Windows Multimedia Audio API.
            
            play_answer(answer_text): Converts the answer text to speech, and plays the synthesized speech using the Windows Multimedia
                                    Audio API.
            
            talk(): Initiates and manages the conversation with the user through the microphone and speakers, processing speech-to-text,
                    text-to-speech, and generating responses using OpenAI's GPT-4 model.
    """

    def __init__(self, logging_level=logging.DEBUG):
        """
            Initializes the VoiceAssistant class with the given parameters.

            Args:
            sampling_frequency (int, optional): The sampling frequency for audio processing. Defaults to 16000.
            channels (int, optional): The number of audio channels. Defaults to 1.
            logging_level (int, optional): The logging level for the VoiceAssistant logger. Defaults to logging.DEBUG.

            Attributes:
            logger (logging.Logger): The logger object for the VoiceAssistant.
            sampling_frequency (int): The sampling frequency for audio processing.
            channels (int): The number of audio channels.
            messages (list): A list of initial instructions for the conversation with a 7-year-old boy named Nikita.
            """
        super().__init__(role_message='You are helpful assistant', logging_level=logging_level)

        #Set logging
        self.logger = logging.getLogger('VoiceAssistantPC')
        self.logger.setLevel(logging_level)
        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()
        ch = logging.StreamHandler()
        ch.setLevel(logging_level)
        self.logger.addHandler(ch)

    def record_voice_from_microphone(self, record_duration_sec=5):
        """Records voice from the microphone for a specified duration and returns a BytesIO stream of the recorded sound.
        
            This function uses the sounddevice library to record the user's voice from the microphone for the given duration
            (in seconds), and converts the recorded sound into a BytesIO stream. The function also logs the recording progress.

            Args:
                record_duration_sec (int, optional): The duration of the recording in seconds. Defaults to 5.

            Returns:
                io.BytesIO: A BytesIO stream containing the recorded sound data.

            Example:
                voice_recorder = VoiceRecorder()
                recorded_voice_stream = voice_recorder.record_voice_from_microphone(record_duration_sec=10)

            Note:
                This function requires the sounddevice and numpy libraries to be installed.
            """

        print(f'Speak {record_duration_sec} seconds ... ')
        sampling_frequency = 16000
        channels = 1
        #Record sound
        recorded_voice = sounddevice.rec(int( record_duration_sec * sampling_frequency), 
                                samplerate = sampling_frequency, channels = channels)
        for i in range(record_duration_sec, 1, -1):
            self.logger.info(f"{i}")
            time.sleep(1)
        sounddevice.wait()
        self.logger.debug(f'Recorded {recorded_voice.shape[0]} bytes.')

        #Convert sound to BytesIO stream
        recorded_voice_int = (recorded_voice * 32767).astype(np.int16)

        byte_io = io.BytesIO()
        write(byte_io, sampling_frequency, recorded_voice_int)
        #write('temp.wav', self.sampling_frequency, recorded_voice_int)
        #result_bytes_wav = byte_io.read() #Finally result_bytes_wav has type bytes, it will be given to google speech to text as parameter

        return byte_io

    def ask_question(self, record_duration_sec=5):
        
        #Records voice from the microphone for a specified duration and returns a BytesIO stream of the recorded sound.
        speech_bytes = self.record_voice_from_microphone(record_duration_sec=record_duration_sec)

        #Convert speech data in byte_io to text using the openai_package.
        question_text = self.convert_speech_to_text(speech_bytes)
        
        self.logger.debug(f"Question text: {question_text}")
        
        return question_text

    def play_mp3(self, mp3_bytes):
        """Plays the given MP3 audio bytes using the Windows Multimedia Audio API.

            This function takes the MP3 audio bytes, converts them to WAV format using the PyDub library, and plays the
            resulting WAV audio using the Windows Multimedia Audio API (win32api).

            Args:
                mp3_bytes (bytes): The MP3 audio bytes to be played.

            Returns:
                None

            Example:
                audio_player = AudioPlayer()
                audio_player.play_mp3(mp3_audio_bytes)

            Note:
                This function requires the PyDub library to be installed and is platform-dependent, as it relies on the
                Windows Multimedia Audio API.
            """
        pydub_obj = AudioSegment.from_file(io.BytesIO(mp3_bytes), format='mp3')
        wave_buffer = io.BytesIO()
        pydub_obj.export(wave_buffer, format='wav')  # Convert To Wave
        wave_buffer.seek(0)  # Move Cursor To The Start Of The File
        winaudio.play_wave_sound(wave_buffer, winaudio.SND_SYNC)
        wave_buffer.close()
        return

    def play_answer(self, answer_text):
        # Converts the given text to speech and returns an AudioSegment object
        answer_audio_segment = self.convert_text_to_speech(answer_text)

        # Convert the AudioSegment object to raw bytes
        answer_mp3_bytes = io.BytesIO()
        answer_audio_segment.export(answer_mp3_bytes, format="mp3")

        # Play the raw MP3 bytes
        self.play_mp3(answer_mp3_bytes.getvalue())

    def talk(self):
        while True:
            #1. Records voice from the microphone for a specified duration and returns a BytesIO stream of the recorded sound.
            #2. Convert speech data in byte_io to text using the openai_package.
            question_text = self.ask_question(record_duration_sec=7)

            #3. Sends a list of messages to OpenAI's GPT-4 model for generating a response and appends the received response to the messages list.
            answer = self.ask_openai(question_text)

            #4. Converts the given text to speech using Google Text-to-Speech API and saves the result as an MP3 file.
            #5. Plays the given MP3 audio bytes using the Windows Multimedia Audio API.
            self.play_answer(answer)

            pressed_key = input('Press any key ...')
            if pressed_key == 'q':
                break

if __name__ == "__main__":
    print('Starting ....')
    assistant = VoiceAssistantPC(logging_level=logging.DEBUG)
    assistant.talk()