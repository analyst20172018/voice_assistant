import requests
import io
import logging
import os

class TelegramBot:
	"""
		A class representing a Telegram bot that can send messages and photos to users.

		Attributes:
		-----------
		bot_name : str
			The name of the bot.
		bot_token : str
			The unique bot token provided by the BotFather on Telegram.

		Methods:
		--------
		get_updates():
			Fetches the updates from the bot's server.

		send_message(chat_id: int, text: str) -> bool:
			Sends a text message to a user specified by the chat_id.

		send_photo(chat_id: int, image: any) -> bool:
			Sends a photo to a user specified by the chat_id.
    """

	bot_name = os.environ.get('TELEGRAM_BOT_NAME')
	BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
	TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

	def __init__(self, logging_level=logging.DEBUG):
		#Set logging
		self.logger = logging.getLogger('TelegramBot')
		self.logger.setLevel(logging_level)
		if (self.logger.hasHandlers()):
			self.logger.handlers.clear()
		ch = logging.StreamHandler()
		ch.setLevel(logging_level)
		self.logger.addHandler(ch)

	def get_updates(self, offset=None):
		"""
			Fetches the updates from the bot's server.

			Returns:
			--------
			dict:
				A dictionary containing the updates in JSON format.
			"""
		
		params = {}
		
		if offset:
			params['offset'] = offset

		response = requests.get(f"{self.TELEGRAM_API_URL}/getUpdates", params=params)
		return response.json()
	
	def download_voice_file(self, file_id):
		"""
			Downloads a voice file specified by the file_id from Telegram's server.

			This method takes the file_id of a voice file and downloads it using the
			Telegram API. It stores the voice file as a BytesIO buffer, which can be
			used directly in the application or saved to a file.

			Parameters:
			-----------
			file_id : str
				The unique identifier for the voice file to be downloaded.

			Returns:
			--------
			io.BytesIO:
				A BytesIO buffer containing the downloaded voice file data. The buffer's
				file pointer is set to the beginning of the data.

			Raises:
			-------
			requests.exceptions.RequestException:
				If there's an issue with the HTTP request to the Telegram API.
			"""
		params = {'file_id': file_id}
		response = requests.get(f"{self.TELEGRAM_API_URL}/getFile", params=params)
		file_info = response.json()['result']
		file_path = file_info['file_path']
		file_url = f'https://api.telegram.org/file/bot{self.BOT_TOKEN}/{file_path}'
		
		response = requests.get(file_url, stream=True)
		voice_data = io.BytesIO()
		for chunk in response.iter_content(chunk_size=8192):
			voice_data.write(chunk)
    
		# Reset the buffer's file pointer to the beginning
		voice_data.seek(0)
		return voice_data

	def send_message(self, chat_id, text, parse_mode=None):
		"""
			Sends a text message to a user specified by the chat_id.

			Parameters:
			-----------
			chat_id : int
				The unique identifier for the target chat.
			text : str
				The text message to be sent.

			Returns:
			--------
			bool:
				True if the message was sent successfully, False otherwise.
        """
		message_data = {'chat_id': chat_id, 'text':text, 'parse_mode': parse_mode}
	
		try:
			request = requests.post(f"{self.TELEGRAM_API_URL}/sendMessage", data=message_data) 
		except:
			print('Send message error')
			return False

		if not request.status_code == 200: return False
		return True

	def send_photo(self, chat_id, image):
		"""
			Sends a photo to a user specified by the chat_id.

			Parameters:
			-----------
			chat_id : int
				The unique identifier for the target chat.
			image : any
				The image to be sent, either as a file or as a file-like object (e.g., a BytesIO buffer).

			Returns:
			--------
			bool:
				True if the photo was sent successfully, False otherwise.
        """
		message_data = {'chat_id': chat_id}
		files = {'photo': image}
	
		try:
			request = requests.post(self.api_url + '/sendPhoto', data=message_data, files=files) 
		except:
			print('Send message error')
			return False

		if not request.status_code == 200: return False
		return True
