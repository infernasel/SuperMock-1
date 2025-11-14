"""
Simple Echo Bot Example for SuperMock

This example demonstrates how to create a simple echo bot that works with SuperMock.
Compatible with python-telegram-bot library.
"""

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "👋 Hello! I'm an echo bot.\n"
        "Send me any message and I'll echo it back!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "📖 Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n\n"
        "Just send me any text and I'll echo it!"
    )


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message"""
    user_message = update.message.text
    await update.message.reply_text(f"🔄 You said: {user_message}")


def main():
    """Start the bot"""
    # Use the SuperMock server URL instead of real Telegram API
    application = Application.builder() \
        .token("test_token_123") \
        .base_url("http://localhost:8081/bot") \
        .build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    # Start the bot
    print("🤖 Echo Bot is running...")
    print("💡 Make sure SuperMock server is running: supermock server")
    print("💬 Or use interactive chat: supermock chat")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
