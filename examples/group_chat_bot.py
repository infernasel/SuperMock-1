"""
Group Chat Bot Example - Demonstrates group chat simulation

This bot showcases:
- Responding to messages in group chats
- Handling @mentions
- Group commands
- Member join/leave events
"""

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    chat_type = update.effective_chat.type
    
    if chat_type == "private":
        await update.message.reply_text(
            "👋 Hello! Add me to a group to see me in action!"
        )
    else:
        await update.message.reply_text(
            f"👋 Hello group! I'm now active in {update.effective_chat.title}!"
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🤖 *Group Chat Bot Help*

*Commands:*
/start - Initialize the bot
/help - Show this help
/stats - Show group statistics
/about - About this bot

*Features:*
• Responds to @mentions
• Tracks group messages
• Welcomes new members
• Says goodbye to leaving members

Try mentioning me with @mock_bot!
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show group statistics"""
    chat = update.effective_chat
    member_count = await chat.get_member_count() if hasattr(chat, 'get_member_count') else "N/A"
    
    stats = f"""
📊 *Group Statistics*

Chat: {chat.title or 'Private Chat'}
Type: {chat.type}
Members: {member_count}
Chat ID: {chat.id}
    """
    await update.message.reply_text(stats, parse_mode="Markdown")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About the bot"""
    await update.message.reply_text(
        "ℹ️ This is a demo bot for testing group chat features with SuperMock!\n\n"
        "SuperMock allows you to test group chat scenarios locally."
    )


async def handle_member_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle new member joining"""
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        
        await update.message.reply_text(
            f"👋 Welcome {member.first_name} to the group!"
        )


async def handle_member_left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle member leaving"""
    member = update.message.left_chat_member
    if not member.is_bot:
        await update.message.reply_text(
            f"👋 Goodbye {member.first_name}! See you again!"
        )


async def handle_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle when bot is mentioned"""
    text = update.message.text
    
    if "@mock_bot" in text.lower():
        await update.message.reply_text(
            f"Hey {update.effective_user.first_name}! You mentioned me! 👋"
        )


async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular group messages"""
    # Only respond occasionally to avoid spam
    import random
    
    if random.random() < 0.1:  # 10% chance to respond
        await update.message.reply_text(
            "👀 I'm watching the conversation..."
        )


def main():
    """Start the group chat bot"""
    print("🤖 Starting Group Chat Bot Demo...")
    print("💡 Make sure SuperMock is running!")
    print("   Start with: supermock server")
    print()
    
    # Use the SuperMock server URL
    application = Application.builder() \
        .token("group_bot_token") \
        .base_url("http://localhost:8081/bot") \
        .build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("about", about_command))
    
    # Member events
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_member_joined))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_member_left))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mention))

    # Start the bot
    print("✅ Group Chat Bot is running!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
