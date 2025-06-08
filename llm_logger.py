from abc import ABC, abstractmethod
from logging import getLogger, NOTSET, basicConfig, INFO
from logging import Logger as CoreLogger
from typing import Optional
from datetime import datetime

# logger interface
class Logger(ABC):
    @abstractmethod
    def info(self, log:str) -> None:
        pass

    @abstractmethod
    def warning(self, log:str) -> None:
        pass

    @abstractmethod
    def error(self, log:str) -> None:
        pass

# factory
class LoggerFactory:
    def is_logging_enabled(self, logger:Optional[CoreLogger] = None) -> bool:
        logger = logger or getLogger()
        return logger.level != NOTSET
    
    def getLogger(self) -> Logger:
        if(self.is_logging_enabled()):
            return FileLogger()
        else:
            return ConsoleLogger()
        
# concrete logger with singleton pattern
class FileLogger(Logger):
    __logger = None
    __log_file_path = "./llm_logs.txt"

    def info(self, log:str) -> None:
        with open(self.__log_file_path, 'a') as llm_log_file:
            llm_log_file.write(str(datetime.now()) + ' - [INFO] - ' + log + '\n\n')

    def warning(self, log:str) -> None:
        with open(self.__log_file_path, 'a') as llm_log_file:
            llm_log_file.write(str(datetime.now()) + ' - [WARNING] - ' + log + '\n\n')

    def error(self, log:str) -> None:
        with open(self.__log_file_path, 'a') as llm_log_file:
            llm_log_file.write(str(datetime.now()) + ' - [ERROR] - ' + log + '\n\n')

    @classmethod
    def getLogger(cls) -> 'FileLogger':
        if cls.__logger is None:
            cls.__logger = FileLogger()
        return cls.__logger

# concrete logger
class ConsoleLogger(Logger):
    __logger = None

    def info(self, log:str) -> None:
        print(str(datetime.now()) + ' - [INFO] - ' + log)

    def warning(self, log:str) -> None:
        print(str(datetime.now()) + ' - [WARNING] - ' + log)

    def error(self, log:str) -> None:
        print(str(datetime.now()) + ' - [ERROR] - ' + log)

    @classmethod
    def getLogger(cls) -> 'ConsoleLogger':
        if cls.__logger is None:
            cls.__logger = ConsoleLogger()
        return cls.__logger