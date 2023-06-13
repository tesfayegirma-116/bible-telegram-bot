import re
import os
import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from typing import List
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
updater = Updater(BOT_TOKEN)


class BibleBot:

    def __init__(self):
        self.translations = ['KJV', 'NIV', 'ESV', 'NKJV', 'NASB', 'MSG', 'AMP']
        self.selected_translation = ''
        self.selected_book = {}
        self.books_cache = {}

    def create_back_button(self) -> List[List[KeyboardButton]]:
        return [[KeyboardButton(text="⬅️ Back")]]

    def start(self, update: Update, context: CallbackContext):
        welcome_message = "In the beginning was the Word, and the Word was with God, and the Word was God. (John 1:1)"
        update.message.reply_text(welcome_message)
        self.send_translation_selection(update, context)

    def send_translation_selection(self, update: Update, context: CallbackContext):
        translation_buttons = [
            [KeyboardButton(text=translation)] for translation in self.translations
        ] + self.create_back_button()

        reply_markup = ReplyKeyboardMarkup(
            translation_buttons, one_time_keyboard=True)
        update.message.reply_text(
            "Select a translation:", reply_markup=reply_markup)

        context.user_data["chat_state"] = "translation"

    def send_books(self, update: Update, context: CallbackContext):
        books = self.fetch_books()
        if not books:
            update.message.reply_text(
                "Error fetching books. Please try again later.")
            return

        book_buttons = [
            [KeyboardButton(
                text=f'{book["name"]} (select_book_{book["bookid"]})')]
            for book in books
        ] + self.create_back_button()

        reply_markup = ReplyKeyboardMarkup(
            book_buttons, one_time_keyboard=True)
        update.message.reply_text("Select a book:", reply_markup=reply_markup)

        context.user_data["chat_state"] = "book"

    def send_chapters(self, update: Update, context: CallbackContext):
        chapters = self.selected_book['chapters']
        chapter_buttons = [
            [KeyboardButton(text=f'{chapter}')]
            for chapter in range(1, chapters + 1)
        ] + self.create_back_button()

        reply_markup = ReplyKeyboardMarkup(
            chapter_buttons, one_time_keyboard=True)
        update.message.reply_text(
            "Select a chapter:", reply_markup=reply_markup)

        context.user_data["chat_state"] = "chapter"

    def fetch_books(self):
        if self.selected_translation in self.books_cache:
            return self.books_cache[self.selected_translation]

        try:
            response = requests.get(
                f'https://bolls.life/get-books/{self.selected_translation}')
            response.raise_for_status()
            books = response.json()
            self.books_cache[self.selected_translation] = books
            return books
        except requests.exceptions.RequestException as e:
            print(f"Error fetching books: {e}")
            return []

    def select_translation(self, update: Update, context: CallbackContext):
        self.selected_translation = update.message.text
        update.message.reply_text(
            f'Selected translation: {self.selected_translation}')
        self.send_books(update, context)

    def select_book(self, update: Update, context: CallbackContext):
        selected_book_id = int(
            re.search(r'select_book_(\d+)', update.message.text).group(1))
        self.selected_book = next(
            book for book in self.fetch_books() if book["bookid"] == selected_book_id)
        self.send_chapters(update, context)

    def select_chapter(self, update: Update, context: CallbackContext):
        selected_chapter = int(update.message.text)
        chapter_content = self.fetch_chapter(selected_chapter)

        max_message_length = 4096
        for i in range(0, len(chapter_content), max_message_length):
            update.message.reply_text(
                chapter_content[i:i + max_message_length])

    def strip_html_tags(self, text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def fetch_chapter(self, chapter_number):
        book_id = self.selected_book["bookid"]
        try:
            response = requests.get(
                f'https://bolls.life/get-chapter/{self.selected_translation}/{book_id}/{chapter_number}')
            response.raise_for_status()
            verses = response.json()
            formatted_text = f"Chapter {chapter_number} - {self.selected_book['name']} ({self.selected_translation})\n\n"
            for verse in verses:
                verse_text = self.strip_html_tags(
                    verse['text']).replace("<br/>", "")
                formatted_text += f"{verse['verse']}. {verse_text}\n\n"
            return formatted_text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching chapter content: {e}")
            return "Error fetching chapter content. Please try again later."

    def handle_back_button(self, update: Update, context: CallbackContext):
        chat_state = context.user_data.get("chat_state", "translation")
        if chat_state == "chapter":
            self.send_books(update, context)
            context.user_data["chat_state"] = "book"
        elif chat_state == "book":
            self.send_translation_selection(update, context)
            context.user_data["chat_state"] = "translation"


def main():
    bible_bot = BibleBot()
    start_handler = CommandHandler('start', bible_bot.start)
    updater.dispatcher.add_handler(start_handler)

    select_translation_handler = MessageHandler(
        Filters.regex('^({})$'.format('|'.join(bible_bot.translations))),
        bible_bot.select_translation
    )
    updater.dispatcher.add_handler(select_translation_handler)

    select_book_handler = MessageHandler(
        Filters.regex('select_book_\d+'), bible_bot.select_book
    )
    updater.dispatcher.add_handler(select_book_handler)

    select_chapter_handler = MessageHandler(
        Filters.regex('^\d+$'), bible_bot.select_chapter
    )
    updater.dispatcher.add_handler(select_chapter_handler)

    back_button_handler = MessageHandler(
        Filters.regex('^⬅️ Back$'), bible_bot.handle_back_button
    )
    updater.dispatcher.add_handler(back_button_handler)

    updater.start_polling()
    print("Bot is running...")
    updater.idle()


if __name__ == '__main__':
    main()
