
from botengine import (start, help, escrow, prices, price, userinfo, hiveuser, msg,
                       buy, sell, cancel, listorders, notify, button, orderClean,
                       setdailyOrderClean, stopdailyOrderClean, release, back,
                       orderinfo, fees, convert)
from error_callback import error_callback
from config import hcbtoken
from logger import logger

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


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(hcbtoken).build()

    # Manage button callbacks
    application.add_handler(CallbackQueryHandler(button))

    # Manage Flood Limits
    application.add_error_handler(CallbackContext(error_callback))

    # Manage Menú Buttons

    # Add active commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("hiveuser", hiveuser))
    application.add_handler(CommandHandler("buy", buy))
    application.add_handler(CommandHandler("sell", sell))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("listorder", listorders))
    application.add_handler(CommandHandler("userinfo", userinfo))
    application.add_handler(CommandHandler("fees", fees))
    application.add_handler(CommandHandler("prices", prices))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("convert", convert))
    application.add_handler(CommandHandler("escrow", escrow))
    # Admins
    application.add_handler(CommandHandler("msg", msg))
    application.add_handler(CommandHandler("notify", notify))
    application.add_handler(CommandHandler("ordersclean", orderClean))
    application.add_handler(CommandHandler(
        "dailyorderclean", setdailyOrderClean))
    application.add_handler(CommandHandler(
        "stopordersclean", stopdailyOrderClean))
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
