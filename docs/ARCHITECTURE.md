# Project Architecture

## Structure

The project is divided into three main classes, each responsible for its own area.

## Modules and Classes

### `src/bot/main.py` – Entry Point

Creates an instance of the `Bot` class and starts the asynchronous event loop using `asyncio.run()`. This is the highest level of the application.

### `src/bot/slang_bot.py` – `Bot` Class

The main class containing all bot logic.

**Attributes:**

- `slang_dict: dict[str, str]` – slang dictionary (word → definition)
- `stemmer: Stemmer` – instance of the `Stemmer` class
- `parser: Parser` – instance of the `Parser` class

**Methods:**

- `__init__()` – initialization, creates `Stemmer` and `Parser` instances
- `find_words(text: str) -> dict` – searches for slang words in text
- `async start(update, context)` – handler for `/start` command
- `async help_command(update, context)` – handler for `/help` command
- `async stats(update, context)` – handler for `/stats` command
- `async show_words(update, context)` – handler for `/words` command
- `async handle_message(update, context)` – handler for text messages
- `async run()` – starts the bot (loads dictionary, registers handlers, starts polling)

### `src/bot/word_stemmer.py` – `Stemmer` Class

Performs Russian word stemming.

**Method:**

- `stem_russian(word: str) -> str` – removes prefixes, suffixes, and endings, returns the word root

**Internal local lists used within the method:**

- `prefixes` – за, на, по, при, от, до, с, у, в, вы, под, над, раз, рас, пере, про, об
- `suffixes` – ться, тся, ти, ть, ет, ит, ат, ят, ут, ют, вш, вши, ш, ши, and others

### `src/bot/site_parser.py` – `Parser` Class

Responsible for loading and parsing the dictionary from an external website.

**Class attributes:**

- `HEADERS: dict` – HTTP request headers (User-Agent)
- `URL: str` – source website address (https://slovar-slenga.tilda.ws/)

**Methods:**

- `import_from_site() -> dict | None` – main method for loading the dictionary
- `fetch_page_with_retry(session, url, max_retries=3) -> str | None` – loads a page with retry logic
- `parse_words_from_html(html: str) -> dict` – parses HTML and extracts words with definitions

### `src/bot/config.py` – Configuration

Contains the `BOT_TOKEN` variable – the Telegram bot token obtained from [@BotFather](https://t.me/BotFather).

## Diagram

```text
┌─────────────────────────────────────────────────┐
│                     main.py                     │
├─────────────────────────────────────────────────┤
│  bot = Bot()                                    │
│  asyncio.run(bot.run())                         │
└─────────────────────────────────────────────────┘
                        │
                        │ creates and runs
                        ▼
┌─────────────────────────────────────────────────┐
│                      Bot                        │
├─────────────────────────────────────────────────┤
│  + slang_dict : Dict                            │
│  + stemmer : Stemmer                            │
│  + parser : Parser                              │
├─────────────────────────────────────────────────┤
│  + __init__()                                   │
│  + find_words(text) : Dict                      │
│  + start(update, context)                       │
│  + help_command(update, context)                │
│  + stats(update, context)                       │
│  + show_words(update, context)                  │
│  + handle_message(update, context)              │
│  + run()                                        │
└─────────────────────────────────────────────────┘
                        │
                        │ contains
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│            Stemmer              │ │            Parser               │
├─────────────────────────────────┤ ├─────────────────────────────────┤
│                                 │ │  + HEADERS : Dict (class)       │
├─────────────────────────────────┤ │  + URL : str (class)            │
│  + stem_russian(word) : str     │ ├─────────────────────────────────┤
│                                 │ │  + import_from_site()           │
│                                 │ │    : Dict | None                │
│                                 │ │  + fetch_page_with_retry()      │
│                                 │ │    : str | None                 │
│                                 │ │  + parse_words_from_html()      │
│                                 │ │    : Dict                       │
└─────────────────────────────────┘ └─────────────────────────────────┘
```
## Component Interaction

### Bot Startup

- `main.py` creates a `Bot` object
- `bot.run()` is called
- `run()` calls `parser.import_from_site()` to load the dictionary
- `import_from_site()` retrieves HTML via `fetch_page_with_retry()`, then `parse_words_from_html()` extracts words and definitions
- The loaded dictionary is stored in `bot.slang_dict`
- `run()` creates the Telegram application and registers command handlers
- The bot enters polling mode and waits for messages

### Processing a Text Message

- User sends a message
- Telegram API passes the event to the bot
- `MessageHandler` calls `handle_message()`
- `handle_message()` passes the text to `find_words()`
- `find_words()`:
  - Converts text to lowercase
  - Extracts individual words using `re.findall()`
  - For each word, searches in `slang_dict`:
    - exact match
    - stem match (via `stemmer.stem_russian()`)
    - partial match (if the word is longer than 2 characters)
- Found words and definitions are returned as a dictionary
- `handle_message()` formats the response in Markdown
- Response is sent back to the user via Telegram API

### Processing Commands

- User enters a command (e.g., `/stats`)
- `CommandHandler` calls the corresponding method:
  - `/start` → `start()` – welcome message
  - `/help` → `help_command()` – help information
  - `/stats` → `stats()` – dictionary statistics
  - `/words` → `show_words()` – list of all words

## Testing

- Tests are run using `pytest`
- `conftest.py` provides fixtures:
  - `stemmer()` – `Stemmer` instance
  - `parser()` – `Parser` instance
  - `bot()` – `Bot` instance with a preloaded test dictionary
- Tests are organized by markers:
  - `@pytest.mark.stemmer` – stemmer tests
  - `@pytest.mark.parser` – parser tests
  - `@pytest.mark.logic` – bot logic tests

## CI/CD Pipeline (GitHub Actions)

On push to `main`, `develop`, or `feature/tests` branches, and on pull requests to `main` or `develop` branches, automatic checks are triggered:

1. Checkout repository
2. Set up Python 3.11
3. Install dependencies from `requirements.txt` and install `pylint`
4. Run tests via `pytest`
5. Run `pylint` linter to check code quality in the `src/` folder