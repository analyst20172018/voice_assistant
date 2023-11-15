# readme.md

Voice Assistant
===============

This is a simple voice assistant application that demonstrates various functionalities for a helpful assistant. The implementation supports PC and Telegram-based user interactions. It converts speech to text, text to speech, and generates responses using OpenAI's GPT-4 model.

## Features

- Communicates with users via microphone (PC) or Telegram chat (Telegram-based implementation)
- Converts speech to text
- Converts text to speech
- Generates intelligent responses using OpenAI's GPT-4 model

## Requirements

- Python 3
- Google Cloud Text-to-Speech API credentials
- OpenAI API credentials
- Telegram bot credentials

## Installation

1. Clone the repository or download the code:

```
git clone https://github.com/example/voice-assistant.git
```

2. Install the required Python packages using pip:

```
pip install -r requirements.txt
```

3. Set up the necessary API credentials in your environment:

The code will use the file .env (which you should create) in the folder "voice_assistant"

The content of the ".env" file should be the following:
> OPENAI_API_KEY=xxx
> TELEGRAM_BOT_NAME=xxx
> TELEGRAM_BOT_TOKEN=xxx

## Usage

Run the appropriate script for your desired implementation:

### Voice Assistant for PC

1. Run the `voice_assistant_pc.py` script:

```
python voice_assistant_pc.py
```

2. Follow the prompts to ask questions and receive responses from the voice assistant.

### Voice Assistant for Telegram

1. Run the `voice_assistant_telegram.py` script (replace `YOUR_TELEGRAM_USER_ID` with your actual Telegram user ID):

```
python voice_assistant_telegram.py --telegram_user_id YOUR_TELEGRAM_USER_ID
```

2. Start a conversation with your bot in the Telegram app and interact with the voice assistant by sending text or voice messages.

Note: Read the implementation code comments for a more detailed understanding of the voice assistant functionalities.

## VoiceAssistantBasic

The VoiceAssistantBasic class provides a basic implementation of a voice assistant that can communicate with users, convert speech to text, text to speech, and generate responses using OpenAI's GPT-4 model.

Methods:
- convert_speech_to_text
- convert_text_to_speech
- ask_openai

## VoiceAssistantPC

The VoiceAssistantPC class extends VoiceAssistantBasic and provides a PC-based implementation of a voice assistant.

Methods:
- record_voice_from_microphone
- ask_question
- play_mp3
- play_answer
- talk

## VoiceAssistantTelegram

The VoiceAssistantTelegram class extends VoiceAssistantBasic and provides a Telegram-based implementation of a voice assistant.

Methods:
- _convert_ogg_sount_to_wav
- _find_offset_of_the_last_message
- talk
