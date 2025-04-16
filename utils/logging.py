import sys
from loguru import logger

def setup_logger():
    """
    Configure the logger with proper formatting and output.
    """
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
    )
    logger.add(
        "logs/bot.log",
        rotation="10 MB",
        compression="zip",
        level="DEBUG",
        retention="1 week",
    )
    
    return logger