"""
Inline Bot Example - Demonstrates inline mode functionality

This bot showcases:
- Inline queries (@botname query)
- Inline results
- Chosen result callbacks
"""

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Application, InlineQueryHandler, ChosenInlineResultHandler,
    CommandHandler, ContextTypes
)
import uuid


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "👋 Hello! I'm an inline bot.\n\n"
        "Try typing @mock_bot <query> in any chat to use me inline!"
    )


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline queries"""
    query = update.inline_query.query
    
    if not query:
        # Show default results when query is empty
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Welcome!",
                input_message_content=InputTextMessageContent(
                    "👋 Hello from inline mode!"
                ),
                description="Send a welcome message"
            ),
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Help",
                input_message_content=InputTextMessageContent(
                    "ℹ️ Type a search query to find content!"
                ),
                description="Show help information"
            )
        ]
    else:
        # Show search results based on query
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=f"Result: {query}",
                input_message_content=InputTextMessageContent(
                    f"📝 You searched for: *{query}*"
                ),
                description=f"Send message about '{query}'"
            ),
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=f"Uppercase: {query.upper()}",
                input_message_content=InputTextMessageContent(
                    f"🔠 {query.upper()}"
                ),
                description=f"Send '{query}' in uppercase"
            ),
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=f"Length: {len(query)} characters",
                input_message_content=InputTextMessageContent(
                    f"📏 Your query has {len(query)} characters"
                ),
                description="Show query length"
            )
        ]
    
    await update.inline_query.answer(results, cache_time=0)


async def chosen_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle when a user chooses an inline result"""
    result = update.chosen_inline_result
    
    print(f"✅ User chose inline result:")
    print(f"   Result ID: {result.result_id}")
    print(f"   Query: {result.query}")
    print(f"   User: {result.from_user.first_name}")


def main():
    """Start the inline bot"""
    print("🤖 Starting Inline Bot Demo...")
    print("💡 Make sure SuperMock is running!")
    print("   Start with: supermock server")
    print()
    print("📝 In SuperMock, simulate inline queries using:")
    print("   from supermock.utils import InlineModeSimulator")
    print("   inline_sim = InlineModeSimulator(server)")
    print("   inline_sim.send_inline_query('test query')")
    print()
    
    # Use the SuperMock server URL
    application = Application.builder() \
        .token("inline_bot_token") \
        .base_url("http://localhost:8081/bot") \
        .build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(ChosenInlineResultHandler(chosen_result))

    # Start the bot
    print("✅ Inline Bot is running!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
