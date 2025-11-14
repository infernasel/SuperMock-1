"""
Inline Keyboard Bot Example for SuperMock

This example demonstrates how to create a bot with inline keyboard buttons.
Compatible with python-telegram-bot library.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="option_1"),
            InlineKeyboardButton("Option 2", callback_data="option_2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="option_3")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Hello! Choose an option:",
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    
    # Answer the callback query
    await query.answer()
    
    # Edit message text based on selected option
    option_texts = {
        "option_1": "✅ You selected Option 1",
        "option_2": "✅ You selected Option 2",
        "option_3": "✅ You selected Option 3",
    }
    
    text = option_texts.get(query.data, "Unknown option")
    await query.edit_message_text(text=text)


def main():
    """Start the bot"""
    # Use the SuperMock server URL instead of real Telegram API
    application = Application.builder() \
        .token("test_token_456") \
        .base_url("http://localhost:8081/bot") \
        .build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot
    print("🤖 Inline Keyboard Bot is running...")
    print("💡 Make sure SuperMock server is running: supermock server")
    print("💬 Or use interactive chat: supermock chat")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
