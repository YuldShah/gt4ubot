#!/usr/bin/env python3
import asyncio
import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.bot import main
from utils.logging import setup_logger

# Set up the logger
logger = setup_logger()

if __name__ == "__main__":
    try:
        logger.info("Starting Google That For You Bot")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.exception(f"Bot stopped due to error: {e}")