import logging
import requests
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    await update.message.reply_text("Which nation's public celebrations are you interested in? Please provide your country code.")
async def holiday(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    key = update.message.text
    # print(word)
    response = requests.get(
        f'https://calendarific.com/api/v2/holidays?&api_key=nP5EjQWi9KDHNzVOySuULjOKLdgn6oWW&country={key}&year=2024')
    i=1
    if (response.status_code == 200):
        data = response.json()
        holiday = data['response']['holidays']
        for h in range(len(holiday)):
            day = holiday[h]
            holiday_name = day['name']
            date = day['date']['datetime']
            year=date['year']
            month=date['month']
            h_day=date['day']
            country = day['country']['name']
            await update.message.reply_text(f"{i}.Date:  {h_day}-{month}-{year}\nHoliday name:  {holiday_name}\nCountry:  {country}")
            i=i+1



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7357834133:AAHtR1FtPcbwTvl3XLjCgeUa0qhG01ocpfk").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, holiday))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
