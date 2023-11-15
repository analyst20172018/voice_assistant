import logging
import os
from openai import OpenAI
import requests
from dotenv import load_dotenv
from pydub import AudioSegment
import io

class VoiceAssistantBasic:
    """
        The VoiceAssistantBasic class provides a basic implementation of a voice assistant that can communicate with users,
        convert speech to text, text to speech, and generate responses using OpenAI's GPT-4 model. The class is designed to
        be extended for specific platforms or use cases.

        Attributes:
            logger (logging.Logger): The logger object for the VoiceAssistantBasic.
            messages (list): A list of instructions for the conversation with a 7-year-old boy named Nikita.

        Methods:
            convert_speech_to_text(byte_io): Converts speech data in byte_io to text using the openai_package.
            
            convert_text_to_speech(text_to_convert): Converts the given text to speech using Google Text-to-Speech API and
                                                    saves the result as an MP3 file.
            
            ask_openai(question_text): Sends a list of messages to OpenAI's GPT-4 model for generating a response and
                                    appends the received response to the messages list.
    """

    def __init__(self, role_message='You are helpful assistant', logging_level=logging.DEBUG):
        #Set logging
        self.logger = logging.getLogger('VoiceAssistantBasic')
        self.logger.setLevel(logging_level)
        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()
        ch = logging.StreamHandler()
        ch.setLevel(logging_level)
        self.logger.addHandler(ch)

        self.logger.debug("Starting VoiceAssistant ...")
        load_dotenv()
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

        self.messages = [{"role": "system", "content": role_message}]

    def convert_speech_to_text(self, byte_io):
        """
            Converts the input speech data in bytes format to text using the openai_package.

            This method takes an input stream of speech data in bytes format, sends it to the openai_package's speech_to_text
            function, and returns the transcribed text. The method also logs the transcription at the debug level.

            Args:
                byte_io (io.BytesIO): An input stream of speech data as bytes.

            Returns:
                str: The transcribed text from the speech data.

            Example:
                with open("path/to/audio/file", "rb") as audio_file:
                    byte_io = io.BytesIO(audio_file.read())
                    text = self.convert_speech_to_text(byte_io)
                    print(text)
        """
        url = "https://api.openai.com/v1/audio/transcriptions"
    
        headers = {
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        }
        data = {
            "model": "whisper-1",
        }

        # Reset the BytesIO object's position to the beginning
        byte_io.seek(0)

        # Directly use the byte_io object as the audio data source
        files = {"file": ("openai.wav", byte_io, "audio/wav")}
        response = requests.post(url, headers=headers, data=data, files=files)
        response = response.json()

        self.logger.debug(f'Transcription: {response["text"]}')
        return response["text"]

    def convert_text_to_speech(self, text_to_convert):
        response = self.client.audio.speech.create(
                                    model="tts-1-hd",
                                    voice="onyx",
                                    input=r"\n\n" + text_to_convert,
                                            )

        # Convert the binary response content to a byte stream
        byte_stream = io.BytesIO(response.content)

        # Read the audio data from the byte stream
        audio = AudioSegment.from_file(byte_stream, format="mp3")
        return audio

    def ask_openai(self, question_text):
        """
            Sends a question to OpenAI's GPT-4 model and generates a response based on the conversation history.

            This method appends the question text to the messages list and sends the updated list of messages to the GPT-4 model.
            It then receives a generated response, adds it to the messages list, and returns the content of the response.

            Args:
                question_text (str): The question text to be sent to the GPT-4 model.

            Returns:
                str: The content of the generated response from the GPT-4 model.

            Example:
                question_text = "What is the capital of France?"
                response_content = self.ask_openai(question_text)
                print(response_content)

            Note:
                This method requires the openai library installed and valid OpenAI API credentials.
        """
        self.logger.debug(f"Asking OpenAI...")
        self.messages.append({"role": "user", "content": question_text})

        response = self.client.chat.completions.create(
                        model="gpt-4",
                        messages=self.messages,
                        )
        
        self.messages.append(response.choices[0].message)
        answer = response.choices[0].message.content

        self.logger.debug(f"Answer: {answer}")
        return answer