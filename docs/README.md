# RU-SlangBot-CHIL (Russian Slang Bot)

Telegram bot for automatic detection and explanation of Russian slang words. The bot analyzes text messages, finds slang expressions using stemming and partial matching, and provides definitions from a curated dictionary.

## Installation

pip install -r requirements.txt

## Usage

Run the bot:

python -m src.bot.main

## Features

- **Automatic slang detection** - analyzes any text message and identifies slang words
- **Stemming support** - finds slang even in modified forms 
- **Built-in dictionary**  loaded from an external source 
- **Partial matching** - detects slang even when part of a longer word
- **Case insensitive** - works with any capitalization
- **Dictionary statistics** - view word count and source information
- **Full word list** - browse all available slang words with /words

## Architecture

The project follows an object-oriented, asynchronous, event-driven architecture:

- **Bot class** (src/bot/slang_bot.py) - main logic, command handlers, slang search
- **Stemmer class** (src/bot/word_stemmer.py) - Russian word stemming (removes prefixes, suffixes, endings)
- **Parser class** (src/bot/site_parser.py) - loads and parses the slang dictionary from an external website
- **Entry point** (src/bot/main.py) - creates the Bot instance and starts the async event loop

The bot uses python-telegram-bot for Telegram API interaction and asyncio for non-blocking concurrent message processing.

## Contributors

- Chevtaeva Elena
- Shvedova Viktoriya
- Tarasenko Khristina