import logging
import os

from google import genai
from google.genai import types
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key="GEMINI_API_KEY")

from dotenv import load_dotenv
load_dotenv()  # take environment variables

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments: update and context
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


# Echo the user message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #await update.message.reply_text(update.message.text)
    await update.message.reply_text(huyGemini(update.message.text))


def huyGemini(input):
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        config=types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain"
        ),
        contents = [
            "input: Как дела?",
            "output: Хуела",
            "input: Я думаю пойти скоро в Дискорд",
            "output: Хуекорд",
            "input: Сегодня в Тбилиси очень жарко",
            "output: Хуярко",
            "input: Кто так называется — тот сам так называется",
            "output: Хуяется",
            "input: Привет",
            "output: Хует",
            "input: Что ты думаешь о Трампе?",
            "output: Хуямпе",
            "input: ",
            "output: ",
        ]
    )

    return response.text
    


def main() -> None:
    # Start the bot
    # Create the Application and pass it your bot's token
    TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Once message is received — echo it
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()