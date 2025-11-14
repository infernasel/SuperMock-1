"""
Advanced Bot Example - Demonstrates all SuperMock features

This bot showcases:
- Text messages
- Photos, videos, audio
- Inline keyboards
- Polls
- Location sharing
- Chat actions
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, filters, ContextTypes
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with main menu"""
    keyboard = [
        [
            InlineKeyboardButton("📸 Send Photo", callback_data="photo"),
            InlineKeyboardButton("🎥 Send Video", callback_data="video"),
        ],
        [
            InlineKeyboardButton("🎵 Send Audio", callback_data="audio"),
            InlineKeyboardButton("📊 Send Poll", callback_data="poll"),
        ],
        [
            InlineKeyboardButton("📍 Send Location", callback_data="location"),
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 *Advanced Bot Demo*\n\n"
        "Welcome! This bot demonstrates all SuperMock features.\n"
        "Choose an option below:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help information"""
    help_text = """
🤖 *Advanced Bot Help*

*Available Commands:*
/start - Show main menu
/help - Show this help
/media - Send media example
/poll - Create a poll
/location - Share location
/echo <text> - Echo your message

*Features:*
✅ Text messages
✅ Photos and videos
✅ Audio files
✅ Polls
✅ Location sharing
✅ Inline keyboards
✅ Callback queries

All powered by SuperMock! 🚀
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def media_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send various media types"""
    await update.message.reply_text("📸 Sending photo...")
    await update.message.reply_photo(
        photo="https://example.com/photo.jpg",
        caption="This is a mock photo!"
    )


async def poll_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create and send a poll"""
    await update.message.reply_poll(
        question="Which feature do you like most?",
        options=[
            "Terminal Chat UI",
            "Mock API Server",
            "Easy Configuration",
            "Docker Support"
        ],
        is_anonymous=True
    )


async def location_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send location"""
    await update.message.reply_location(
        latitude=55.751244,
        longitude=37.618423
    )
    await update.message.reply_text("📍 This is Moscow, Russia!")


async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo user's text"""
    text = ' '.join(context.args) if context.args else "Nothing to echo!"
    await update.message.reply_text(f"🔄 {text}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    action = query.data
    
    if action == "photo":
        await query.message.reply_photo(
            photo="https://example.com/photo.jpg",
            caption="📸 Here's a mock photo!"
        )
    
    elif action == "video":
        await query.message.reply_video(
            video="https://example.com/video.mp4",
            caption="🎥 Here's a mock video!"
        )
    
    elif action == "audio":
        await query.message.reply_audio(
            audio="https://example.com/audio.mp3",
            caption="🎵 Here's a mock audio!"
        )
    
    elif action == "poll":
        await query.message.reply_poll(
            question="How do you like SuperMock?",
            options=["Excellent! ⭐⭐⭐⭐⭐", "Very Good ⭐⭐⭐⭐", "Good ⭐⭐⭐", "Okay ⭐⭐"],
            is_anonymous=False
        )
    
    elif action == "location":
        await query.message.reply_location(
            latitude=55.751244,
            longitude=37.618423
        )
        await query.message.reply_text("📍 Moscow, Russia")
    
    elif action == "help":
        await query.message.reply_text(
            "ℹ️ *Help Information*\n\n"
            "Use the buttons to test different features.\n"
            "Type /help for more information.",
            parse_mode="Markdown"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages"""
    user_text = update.message.text
    
    # Simulate typing action
    await update.message.chat.send_action(action="typing")
    
    response = f"💬 You said: *{user_text}*\n\n"
    response += "I'm a demo bot running on SuperMock!\n"
    response += "Try /start to see what I can do! 🚀"
    
    await update.message.reply_text(response, parse_mode="Markdown")


def main():
    """Start the advanced bot"""
    print("🚀 Starting Advanced Bot Demo...")
    print("💡 Make sure SuperMock is running!")
    print("   Start with: supermock server")
    print("   Or use: supermock chat (for interactive testing)")
    print()
    
    # Use the SuperMock server URL
    application = Application.builder() \
        .token("advanced_bot_token") \
        .base_url("http://localhost:8081/bot") \
        .build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("media", media_command))
    application.add_handler(CommandHandler("poll", poll_command))
    application.add_handler(CommandHandler("location", location_command))
    application.add_handler(CommandHandler("echo", echo_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("✅ Advanced Bot is running!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
