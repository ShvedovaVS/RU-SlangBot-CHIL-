**Basic Information**

The project API is a set of classes and methods for interacting with the bot's functionality. It is divided into three independent modules that can be used together or separately.

| **Module**      | **Class** | **Purpose**              |
| --------------- | --------- | ------------------------ |
| word_stemmer.py | Stemmer   | Russian word stemming    |
| site_parser.py  | Parser    | Slang dictionary loading |
| slang_bot.py    | Bot       | Main Telegram bot logic  |

**Class Stemmer**

**Purpose**

Stemming of Russian words (reducing to root form).

**Import**

from word_stemmer import Stemmer

**Constructor**

stemmer = Stemmer()

**Methods**

**stem_russian(self, word)**

Reduces a word to its root form.

**Parameters:**

- word: type - str

Description: Word to process

**Return value:** str - root form of the word.

**Algorithm:**

- Convert word to lowercase
- Remove prefixes (prefixes list)
- Remove suffixes and endings (suffixes list)
- Return processed word

**Class Parser**

**Purpose**

Loading the slang dictionary from an external source.

**Import**

from site_parser import Parser

**Constructor**

parser = Parser()

**Attributes**

HEADERS:

- Type: dict
- Access: class
- Description: HTTP request headers (User-Agent)

URL:

- Type: str
- Access: class
- Description: Source website URL

**Methods**

- **import_from_site(self)**

Main method for loading the dictionary. Performs HTTP request via fetch_page_with_retry() and parsing via parse_words_from_html().

**Parameters:** self

**Return value:**

- dict\[str, str\] - dictionary of the form {word: definition} on success
- None - on error

- **fetch_page_with_retry(self, session, url, max_retries=3)**

Loads a page with retry logic on error.

**Parameters:**

- session: type - requests.Session

Description: Session for HTTP requests

- url: type - str

Description: Page URL

- max_retries: type - int

Description: Maximum number of attempts (default 3)

**Return value:**

- str - HTML page content on successful load
- None - on error after all attempts

**Algorithm:**

- Loop for max_retries attempts
- On retry attempts - random delay between 2 and 5 seconds
- Execute GET request with 30 second timeout
- On status 200 - return HTML content
- **parse_words_from_html(self, html)**

Parses HTML page and extracts words with definitions.

**Parameters:**

- html: type - str

Description: HTML page content

**Return value:** dict\[str, str\] - dictionary of the form {word: definition}

**Algorithm:**

- Find all blocks with class containing t-text and t-text_md
- Split HTML by &lt;br/&gt; tags
- Find bold words (&lt;strong&gt;...&lt;/strong&gt;) as dictionary keys
- Collect multi-line definitions
- Remove dashes and numbering

**Logging:** outputs number of found blocks and words

**Class Bot**

**Purpose**

Main Telegram bot class. Manages command and message handling, slang search.

**Import**

from slang_bot import Bot

from config import BOT_TOKEN

**Constructor**

bot = Bot()

**Attributes**:

slang_dict

- Type: dict\[str, str\]
- Access: public
- Description: Slang dictionary (loaded via run())

stemmer

- Type: Stemmer
- Access: public
- Description: Stemmer class instance

parser

- Type: Parser
- Access: public
- Description: Parser class instance

**Methods**

**find_words(self, text: str) -> dict**

Searches for slang words in text.

**Parameters:**

- text: type - str

Description: Text to analyze

**Return value:** dict\[str, str\] - dictionary of found words and definitions. Empty dictionary if nothing found.

**Algorithm:**

- Convert text to lowercase
- Extract words via re.findall(r'\\b\[а-яёa-z\]+\\b', text)
- For each word:
  - Exact match in slang_dict
  - Stem match via stemmer.stem_russian()
  - Partial match (if word longer than 2 characters)

**async run(self)**

Starts the bot.

**Actions:**

- Load dictionary via parser.import_from_site()
- Initialize Telegram application with token from config.BOT_TOKEN
- Register command handlers
- Start polling for new messages
- Wait for shutdown (Ctrl+C)

**Logging:**

- 📚 Загрузка словаря...
- ✅ Готово
- 🚀 Бот запущен...
- 👋 Остановка бота... (on shutdown)

**async start(self, update: Update, context: ContextTypes.DEFAULT_TYPE)**

Handler for /start command. Sends welcome message.

**Parameters:**

- update: type - telegram.Update

Description: Update object from Telegram

- context: type - telegram.ext.ContextTypes.DEFAULT_TYPE

Description: Handler context

**async help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE)**

Handler for /help command. Sends bot usage help (Markdown format).

**async stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE)**

Handler for /stats command. Sends dictionary statistics:

- Word count (len(self.slang_dict))
- Language (Russian)
- Dictionary source

**async show_words(self, update: Update, context: ContextTypes.DEFAULT_TYPE)**

Handler for /words command. Sends list of all words in the dictionary.

- Words sorted alphabetically
- Split into chunks of 50 words
- First chunk contains hint: "To find out the meaning of a word, just send it in the chat!"

**async handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE)**

Handler for text messages (non-commands).

- Calls find_words() to analyze text
- If words found - sends them with definitions in Markdown format
- If no words found - sends message indicating no slang detected

**Exceptions**

Missing config.py or BOT_TOKEN - Import error, bot does not start

Dictionary failed to load - self.slang_dict = {}, bot works with empty dictionary

Telegram API unavailable - Exception in application.run_polling()

Shutdown via Ctrl+C - Graceful shutdown: stop polling, close application

**Used Libraries**

**python-telegram-bot (20.0)**  
Interaction with Telegram Bot API. Used in slang_bot.py. Provides classes Application, Update, ContextTypes and handlers CommandHandler, MessageHandler, filters.

**requests (2.32.5)**  
Performs HTTP requests to the dictionary source website. Used in site_parser.py.

**beautifulsoup4 (4.14.3)**  
Parses HTML pages. Used in site_parser.py to extract blocks with classes t-text and t-text_md.

**asyncio**  
Built-in Python library for asynchronous operations. Used in slang_bot.py and main.py. Allows the bot to process multiple messages simultaneously.

**re**  
Built-in library for regular expressions. Used in slang_bot.py to extract words from text (\\b\[а-яёa-z\]+\\b), and in site_parser.py to split HTML by &lt;br/&gt; tags and search for bold words.

**random**  
Built-in library for random number generation. Used in site_parser.py to create random delays (between 2 and 5 seconds) between retry attempts.

**time (sleep)**  
Built-in library. Used in site_parser.py to create pauses between page load attempts.