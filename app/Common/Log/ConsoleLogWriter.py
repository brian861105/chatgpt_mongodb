import logging
from iLogWriter import iLogWriter

class ConsoleLogWriter(iLogWriter):
    def __init__(self):
        self.logger = logging.getLogger('console_logger')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def log_debug(self, message: str) -> None:
        return super().log_debug(message)
    def log_info(self, message: str) -> None:
        return super().log_info(message)
    def log_error(self, message: str) -> None:
        return super().log_error(message)
    def log_critical(self, message: str) -> None:
        return super().log_critical(message)
    def log_warning(self, message: str) -> None:
        return super().log_warning(message)