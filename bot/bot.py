import os
from aiogram import Bot, Dispatcher, types, F, html
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

import sys
import asyncio

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging import setup_logger
from utils.url_utils import create_google_search_url

# Initialize logger
logger = setup_logger()

# Load environment variables
load_dotenv()

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
@dp.message(F.text == "ℹ️ Get info")
async def cmd_start(message: types.Message):
    """Handle /start command"""
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        f"Hi {message.from_user.full_name}! 👋\n\n"
        f"Send me any text and I'll convert it to a Google search link.\n\n"
        f"You can also use me in inline mode by typing @lgtfy_bot in any chat.",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="ℹ️ Get info")]],
            resize_keyboard=True,
            input_field_placeholder="Enter your query..."
        )
    )

@dp.message(F.text)
async def handle_text(message: types.Message):
    """Process text messages and convert to Google search links"""
    text = message.text
    logger.info(f"Received text from user {message.from_user.id}: {text}")
    
    # Generate Google search URL
    search_url = create_google_search_url(text)
    
    # Create inline keyboard with button to copy the link
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Copy Link", copy_text=types.CopyTextButton(text=search_url))]
    ])
    
    await message.answer(
        f"Here's your Google search link (tap to copy):\n\n{html.code(search_url)}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.inline_query()
async def inline_query_handler(query: types.InlineQuery):
    """Handle inline queries"""
    text = query.query
    
    if not text:
        # Return an article that prompts the user to enter a search term
        await query.answer(
            results=[
                types.InlineQueryResultArticle(
                    id="empty",
                    title="Enter text to convert to a Google search link",
                    input_message_content=types.InputTextMessageContent(
                        message_text="Please enter a search term after @lgtfy_bot"
                    )
                )
            ],
            cache_time=5
        )
        return
    
    # Generate Google search URL
    search_url = create_google_search_url(text)
    
    # Create inline keyboard with button to copy link
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Google That!", url=search_url)]
    ])
    
    # Create the inline result
    result = types.InlineQueryResultArticle(
        id=str(hash(text)),
        title=f"Send Google Search link for: {text}",
        description=search_url,
        input_message_content=types.InputTextMessageContent(
            message_text=f"Here is your Google Search link for:\n<b>{text}</b>",
            parse_mode="HTML"
        ),
        reply_markup=keyboard
    )
    
    logger.info(f"Inline query from user {query.from_user.id}: {text}")
    await query.answer([result], cache_time=300)

async def main():
    """Main function to start the bot"""
    logger.info("Starting bot")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())