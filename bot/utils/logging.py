import logging
from logging.handlers import RotatingFileHandler
import os

from attr import dataclass


@dataclass
class Colors:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BOLD = '\033[1m'
    RESET = "\033[0m"


class ConsoleFormatter(logging.Formatter):
    def format(self, record):
        lvl = record.levelname
        if lvl == "INFO":
            record.levelname = f"{Colors.BOLD}{Colors.GREEN}[I]{Colors.RESET}"
        elif lvl == "WARNING":
            record.levelname = f"{Colors.BOLD}{Colors.YELLOW}[W]{Colors.RESET}"
        elif lvl == "DEBUG":
            record.levelname = f"{Colors.BOLD}{Colors.BLUE}[D]{Colors.RESET}"
        elif lvl == "ERROR":
            record.levelname = f"{Colors.BOLD}{Colors.RED}[E]{Colors.RESET}"
        return super().format(record)
    

class FileFormatter(logging.Formatter):
    def format(self, record):
        lvl = record.levelname
        if lvl == "INFO":
            record.levelname = "[I]"
        elif lvl == "WARNING":
            record.levelname = "[W]"
        elif lvl == "DEBUG":
            record.levelname = "[D]"
        elif lvl == "ERROR":
            record.levelname = "[E]"
        return super().format(record)


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("aiogram_bot")
    logger.setLevel(logging.DEBUG)

    consoleformatter = ConsoleFormatter("%(levelname)s [%(filename)s:%(lineno)-3d] %(message)s")
    fileformatter = FileFormatter("%(levelname)s [%(filename)s:%(lineno)-3d] %(message)s")


    log_path = os.path.join("logs", "bot.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    fh = RotatingFileHandler(
        log_path, 
        maxBytes=10_000_000, 
        backupCount=5, 
        encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fileformatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(consoleformatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger