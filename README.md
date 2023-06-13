# BibleBot

BibleBot is a Telegram bot that allows users to search and read the Bible. The bot supports multiple translations and allows users to navigate through the books and chapters of the Bible to read specific verses.

## Getting Started

To use the BibleBot, you will need to have a Telegram account and install the Telegram app on your device.

To start using the BibleBot, follow these steps:

1. Open the Telegram app and search for the BibleBot by typing `@bible_bot` in the search bar.
2. Start a conversation with the BibleBot by sending the `/start` command.
3. The BibleBot will ask you to select a Bible translation. Choose one of the available translations by clicking on the corresponding button.
4. The BibleBot will then present you with a list of books from the selected translation. Choose a book by clicking on the corresponding button.
5. The BibleBot will then present you with a list of chapters from the selected book. Choose a chapter by clicking on the corresponding button.
6. The BibleBot will then send you the text of the selected chapter, broken up into separate messages if necessary.

To go back to a previous step in the conversation, click on the "⬅️ Back" button.

## Supported Translations

The BibleBot currently supports the following translations:

- KJV (King James Version)
- NIV (New International Version)
- ESV (English Standard Version)
- NKJV (New King James Version)
- NASB (New American Standard Bible)
- MSG (The Message)
- AMP (Amplified Bible)

## Development

If you want to modify or contribute to the BibleBot code, you will need to follow these steps:

1. Clone the BibleBot repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Create a new Telegram bot and obtain an API token from the BotFather.
4. Replace the `BOT_TOKEN` variable in the `biblebot.py` file with your own API token.
5. Run the `biblebot.py` file to start the bot.




## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Run Locally

Clone the project

```bash
  git clone https://github.com/tesfayegirma-116/bible-telegram-bot.git
```

Go to the project directory

```bash
  cd bible-telegram-bot
```

Run docker

```bash
  docker build -t bible_bot .
```

Start the bot

```bash
  docker run bible_bot
```


## Authors

- [@tesfayegirma](https://github.com/tesfayegirma-116)

