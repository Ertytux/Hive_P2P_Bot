
from botengine import (start, escrow, prices, price, userinfo, hiveuser, msg,
                       buy, sell, cancel, listorders, notify, button, orderClean,
                       setdailyOrderClean, stopdailyOrderClean, release, back, orderinfo)

from config import hcbtoken

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This version is not compatible with your current PTB version {TG_VER}."
    )

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Retries hand to avoid Flood Limits
MAX_RETRIES = 10
RETRY_INTERVAL = 5


async def error_callback(update: Update, context: CallbackContext) -> None:
    retries = context.error_retries
    if retries < MAX_RETRIES:
        logger.warning(
            f"Error in the request. Retry in {RETRY_INTERVAL} seconds...")
        context.error_retries += 1
        await context.job_queue.run_once(error_callback, RETRY_INTERVAL, context=update)
    else:
        logger.error(
            "The maximum number of retries was reached. The request could not be processed.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(hcbtoken).build()

    # Add active commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("escrow", escrow))
    application.add_handler(CommandHandler("hiveuser", hiveuser))
    application.add_handler(CommandHandler("userinfo", userinfo))
    application.add_handler(CommandHandler("msg", msg))
    application.add_handler(CommandHandler("notify", notify))
    application.add_handler(CommandHandler("buy", buy))
    application.add_handler(CommandHandler("sell", sell))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("listorder", listorders))
    application.add_handler(CommandHandler("prices", prices))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CallbackQueryHandler(button))

    # Manage Flood Limits
    application.add_error_handler(CallbackContext(error_callback))

    # Admins
    application.add_handler(CommandHandler(
        "dailyorderclean", setdailyOrderClean))
    application.add_handler(CommandHandler(
        "stopordersclean", stopdailyOrderClean))
    application.add_handler(CommandHandler("ordersclean", orderClean))
    application.add_handler(CommandHandler("release", release))
    application.add_handler(CommandHandler("back", back))
    application.add_handler(CommandHandler("orderinfo", orderinfo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if not hcbtoken:
    print(f"The hcbtoken environment variable is not defined.")
else:
    if __name__ == "__main__":
        main()


