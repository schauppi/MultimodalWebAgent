from colorama import init, Fore, Back, Style
import logging

init()


class ColoredFormatter(logging.Formatter):
    """
    A custom logging formatter that adds color to log messages based on their log level.

    Methods:
        format(record: logging.LogRecord) -> str:
            Formats the log record and adds color to the log message based on the log level.

    """

    COLOR_CODES = {
        "DEBUG": Fore.WHITE,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Back.RED,
    }
    RESET = Style.RESET_ALL

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record and adds color to the log message based on the log level.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with color added.

        """
        color_code = self.COLOR_CODES.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{color_code}{message}{self.RESET}"
