import os
from dotenv import load_dotenv
from maxgram import Bot
from maxgram.keyboards import InlineKeyboard

# Load environment variables
load_dotenv()

# Initialize bot with token from environment
bot = Bot(os.getenv("BOT_TOKEN"))

# Create productivity menu keyboard
productivity_menu = InlineKeyboard(
    [
        {"text": "📋 Create Task", "callback": "create_task"},
    ],
    [
        {"text": "✅ View Tasks", "callback": "view_tasks"},
        {"text": "📊 Statistics", "callback": "stats"}
    ],
    [
        {"text": "⚙️ Settings", "callback": "settings"}
    ]
)

# Handler for bot start
@bot.on("bot_started")
def on_start(context):
    context.reply(
        "👋 Welcome to Productivity Bot!\n\nI'll help you manage your tasks and stay productive.",
        keyboard=productivity_menu
    )

# Handler for /start command
@bot.command("start")
def start_command(context):
    context.reply(
        "🚀 Let's get productive!\n\nChoose an action:",
        keyboard=productivity_menu
    )

# Handler for /help command
@bot.command("help")
def help_command(context):
    help_text = """
📖 **Available Commands:**

/start - Show main menu
/help - Display this help message
/task - Quick task creation
/stats - View your statistics

Simply type your task description to create a new task!
    """
    context.reply(help_text)

# Handler for button callbacks
@bot.on("message_callback")
def handle_callback(context):
    button = context.payload
    
    if button == "create_task":
        context.reply_callback(
            "📝 Please send me your task description.",
            is_current=True
        )
    elif button == "view_tasks":
        context.reply_callback(
            "📋 Your Tasks:\n\n1. Example task\n2. Another task\n\n(This is a placeholder - implement your task storage)",
            keyboard=productivity_menu,
            is_current=True
        )
    elif button == "stats":
        context.reply_callback(
            "📊 Your Statistics:\n\n✅ Completed: 0\n⏳ Pending: 0\n🔥 Streak: 0 days",
            keyboard=productivity_menu,
            is_current=True
        )
    elif button == "settings":
        context.reply_callback(
            "⚙️ Settings:\n\n(Configure your preferences here)",
            keyboard=productivity_menu,
            is_current=True
        )

# Handler for regular messages
@bot.on("message_created")
def handle_message(context):
    if context.message and context.message.get("body") and "text" in context.message["body"]:
        text = context.message["body"]["text"]
        
        # Ignore commands
        if not text.startswith("/"):
            # Treat message as task creation
            context.reply(
                f"✅ Task created: {text}\n\nUse /start to see all your tasks.",
                keyboard=productivity_menu
            )

# Set bot commands for user interface
bot.set_my_commands({
    "start": "Show main menu",
    "help": "Get help",
    "task": "Create new task",
    "stats": "View statistics"
})

# Run the bot
if __name__ == "__main__":
    print("🤖 Bot is starting...")
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
        bot.stop()
