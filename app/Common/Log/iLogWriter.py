from abc import ABC, abstractmethod

class iLogWriter(ABC):
    @abstractmethod
    def log_debug(self, message: str) -> None:
        pass
    def log_info(self, message: str) -> None:
        pass
    def log_warning(self, message: str) -> None:
        pass
    def log_error(self, message: str) -> None:
        pass
    def log_critical(self, message: str) -> None:
        pass