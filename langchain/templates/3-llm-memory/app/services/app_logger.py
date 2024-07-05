import logging
import os

from logging.handlers import RotatingFileHandler

ONE_MB_IN_BYTES = 1000000


class AppLogger:
    def __init__(self, log_dir: str, log_file: str, log_level: int = logging.INFO):
        self.log_dir = log_dir
        self.log_file = log_file
        self.log_file_path = os.path.join(self.log_dir, self.log_file)
        # Ensure log dir exists (don't need to do this for the log file)
        os.makedirs(self.log_dir, exist_ok=True)

        self.log_level = log_level

        self.logger = logging.getLogger("app_logger")
        self.logger.setLevel(self.log_level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        handler = RotatingFileHandler(
            self.log_file_path, maxBytes=ONE_MB_IN_BYTES, backupCount=1
        )
        handler.setLevel(self.log_level)
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def log(self, message: str, *args, **kwargs) -> None:
        if self.logger.isEnabledFor(self.log_level):
            self.logger._log(self.log_level, message, args, **kwargs)

    def clear_log_file(self) -> None:
        with open(self.log_file_path, "w"):
            pass
