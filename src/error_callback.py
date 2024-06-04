from logger import  logger

from telegram import Update
from telegram.ext import CallbackContext

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