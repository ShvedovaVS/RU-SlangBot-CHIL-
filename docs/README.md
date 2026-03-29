# RU-SlangBot-CHIL (Russian Slang Bot)

Telegram bot for automatic detection and explanation of Russian slang words. The bot analyzes text messages, finds slang expressions using stemming and partial matching, and provides definitions from a curated dictionary.

## Documentation

- [Installation and User Guide](INSTALL.md)
- [API Reference](API.md)
- [Architecture](ARCHITECTURE.md)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ShvedovaVS/RU-SlangBot-CHIL-.git
   cd RU-SlangBot-CHIL-
   ```
2. Install dependencies:
    ```bash
   pip install -r requirements.txt
   ```
   
3. Create configuration file src/bot/config.py with your bot token: 
    ```python
   BOT_TOKEN = "your_telegram_bot_token_here"
   ```
Get a token from @BotFather on Telegram.

## Usage

Run the bot from the project root directory:
   ```python
    PYTHONPATH=. python src/bot/main.py
   ```

## Features

- **Automatic slang detection** - analyzes any text message and identifies slang words
- **Stemming support** - finds slang even in modified forms 
- **Built-in dictionary**  loaded from an external source 
- **Partial matching** - detects slang even when part of a longer word
- **Case insensitive** - works with any capitalization
- **Dictionary statistics** - view word count and source information with `/stats`
- **Full word list** - browse all available slang words with `/words`

## Architecture

The project follows an object-oriented, asynchronous, event-driven architecture. See [Architecture](ARCHITECTURE.md) for details.

The project follows an object-oriented, asynchronous, event-driven architecture. See [Architecture](ARCHITECTURE.md) for details.

- **Bot class** (src/bot/slang_bot.py) - main logic, command handlers, slang search coordination
- **SlangAnalyzer class** (src/bot/slang_analyzer.py) - analyzes incoming text, detects slang words using dictionary lookup, stemming, and partial matching
- **Stemmer class** (src/bot/word_stemmer.py) - Russian word stemming (removes prefixes, suffixes, endings)
- **Parser class** (src/bot/site_parser.py) - loads and parses the slang dictionary from an external website
- **Entry point** (src/bot/main.py) - creates the Bot instance and starts the async event loop

The bot uses python-telegram-bot for Telegram API interaction and asyncio for non-blocking concurrent message processing.

## Contributors

- Chevtaeva Elena
- Shvedova Viktoriya
- Tarasenko Khristina