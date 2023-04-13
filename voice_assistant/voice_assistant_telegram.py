import numpy as np
import io
import logging
import time
from pydub import AudioSegment
from voice_assistant_basic import VoiceAssistantBasic
import telegram_bot
import fire


class VoiceAssistantTelegram(VoiceAssistantBasic):
    """
        The VoiceAssistantTelegram class extends VoiceAssistantBasic and provides a Telegram-based implementation of a voice
        assistant that can communicate with users, convert speech to text, text to speech, and generate responses using OpenAI's
        GPT-4 model.

        Attributes:
            logger (logging.Logger): The logger object for the VoiceAssistantTelegram.
            USER_ID (int): The user ID for the target user to communicate with.
            bot (telegram_bot.TelegramBot): The Telegram bot object for interacting with the Telegram API.

        Methods:
            _convert_ogg_sount_to_wav(bytesio_sound): Converts the input OGG sound data in bytes format to WAV format.
            
            _find_offset_of_the_last_message(): Finds the offset for the latest message in the Telegram chat.

            talk(): Initiates and manages the conversation with the target user on Telegram, processing speech-to-text, text-to-speech,
                    and generating responses using OpenAI's GPT-4 model.
    """

    def __init__(self, telegram_user_id, logging_level=logging.DEBUG):
        super().__init__(logging_level)

        #Set logging
        self.logger = logging.getLogger('VoiceAssistantTelegram')
        self.logger.setLevel(logging_level)
        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()
        ch = logging.StreamHandler()
        ch.setLevel(logging_level)
        self.logger.addHandler(ch)

        self.USER_ID = telegram_user_id
        self.bot = telegram_bot.TelegramBot()
    
    def _convert_ogg_sount_to_wav(self, bytesio_sound):
        """
            Converts the input OGG sound data in bytes format to WAV format.

            This method takes an input stream of OGG sound data in bytes format, converts it to WAV format using the PyDub library,
            and returns the converted WAV sound data.

            Args:
                bytesio_sound (io.BytesIO): An input stream of OGG sound data as bytes.

            Returns:
                io.BytesIO: A BytesIO stream containing the converted WAV sound data.

            Example:
                with open("path/to/ogg/file", "rb") as ogg_file:
                    bytesio_sound = io.BytesIO(ogg_file.read())
                    wav_data = self._convert_ogg_sount_to_wav(bytesio_sound)

            Note:
                This method requires the PyDub library installed.
        """
        bytesio_sound.seek(0)
        pydub_obj = AudioSegment.from_ogg(bytesio_sound)
        wave_buffer = io.BytesIO()
        pydub_obj.export(wave_buffer, format='wav')  # Convert To Wave
        wave_buffer.seek(0)  # Move Cursor To The Start Of The File
        return wave_buffer

    def _find_offset_of_the_last_message(self):
        """
            Finds the offset for the latest message in the Telegram chat.

            This method retrieves the updates from the Telegram bot and calculates the offset for the latest message. If no messages
            are found, the method returns None.

            Args:
                None

            Returns:
                int or None: The offset of the latest message or None if no messages are found.

            Example:
                last_message_offset = self._find_offset_of_the_last_message()
                print(last_message_offset)

            Note:
                This method requires the telegram_bot library installed and valid Telegram bot credentials.
        """
        response = self.bot.get_updates()
        if len(response['result']) > 0:
            offset = response["result"][-1]["update_id"] + 1
            self.logger.debug(f"{len(response['result'])} message found. The latest offset is {offset}")
        else:
            self.logger.debug("No messages found.")
            offset = None
        return offset

    def talk(self):
        """
            Initiates and manages the conversation with the target user on Telegram.

            This method loops indefinitely, checking for new messages from the target user on Telegram. When a new message is received,
            it processes the message's text or voice data by converting speech to text (if necessary), generates a response using
            OpenAI's GPT-4 model, and sends the response back to the user as a text message. The conversation history is updated
            accordingly.

            Args:
                None

            Returns:
                None

            Example:
                voice_assistant = VoiceAssistantTelegram()
                voice_assistant.talk()

            Note:
                This method requires the openai, google-cloud-texttospeech, and telegram_bot libraries installed with valid API credentials.
        """
        offset = self._find_offset_of_the_last_message()
        self.bot.send_message(self.USER_ID, 'Привет Никита')

        while True:
            response = self.bot.get_updates(offset=offset)
            #self.logger.debug(f'There are {len(response)} messages.')

            if len(response["result"]) > 0:
                #Check, that this is a message from correct user
                if response['result'][0]['message']['from']['id'] != self.USER_ID:
                    self.logger.critical(f'Message from unauthorized user.')
                    break

                offset = response["result"][0]["update_id"] + 1

                #Get text message
                if "text" in response["result"][0]["message"]:
                    question_text = response["result"][0]["message"]["text"]
                    self.logger.debug(f"Text: {question_text}.")

                #Get voice message and convert it to text
                if "voice" in response["result"][0]["message"]:
                    print('Downloading voice data ...')
                    voice_data = self.bot.download_voice_file(response["result"][0]["message"]["voice"]["file_id"])
                    self.logger.debug(f"Voice file is downloaded.")
                    voice_data_wav = self._convert_ogg_sount_to_wav(voice_data)
                    question_text = self.convert_speech_to_text(voice_data_wav)
                    self.logger.debug(f"Text: {question_text}.")

                #Answer to message
                answer = self.ask_openai(question_text)
                self.bot.send_message(self.USER_ID, answer)
                self.logger.debug(f"Latest offset is: {offset}.")
            
            time.sleep(2)

def main(telegram_user_id):
    print('Starting ....')
    assistant = VoiceAssistantTelegram(telegram_user_id, logging_level=logging.INFO)
    assistant.talk()

if __name__ == "__main__":
    fire.Fire(main)